"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __esm = (fn, res) => function __init() {
  return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/src/config.ts
var import_sdk, configSchematics;
var init_config = __esm({
  "C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/src/config.ts"() {
    "use strict";
    import_sdk = require("@lmstudio/sdk");
    configSchematics = (0, import_sdk.createConfigSchematics)().field(
      "retrievalLimit",
      "numeric",
      {
        int: true,
        min: 1,
        displayName: "Retrieval Limit",
        subtitle: "When retrieval is triggered, this is the maximum number of chunks to return.",
        slider: { min: 1, max: 10, step: 1 }
      },
      3
    ).field(
      "retrievalAffinityThreshold",
      "numeric",
      {
        min: 0,
        max: 1,
        displayName: "Retrieval Affinity Threshold",
        subtitle: "The minimum similarity score for a chunk to be considered relevant.",
        slider: { min: 0, max: 1, step: 0.01 }
      },
      0.5
    ).build();
  }
});

// C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/src/promptPreprocessor.ts
async function preprocess(ctl, userMessage) {
  const userPrompt = userMessage.getText();
  const history = await ctl.pullHistory();
  history.append(userMessage);
  const newFiles = userMessage.getFiles(ctl.client).filter((f) => f.type !== "image");
  const files = history.getAllFiles(ctl.client).filter((f) => f.type !== "image");
  if (newFiles.length > 0) {
    const strategy = await chooseContextInjectionStrategy(ctl, userPrompt, newFiles);
    if (strategy === "inject-full-content") {
      return await prepareDocumentContextInjection(ctl, userMessage);
    } else if (strategy === "retrieval") {
      return await prepareRetrievalResultsContextInjection(ctl, userPrompt, files);
    }
  } else if (files.length > 0) {
    return await prepareRetrievalResultsContextInjection(ctl, userPrompt, files);
  }
  return userMessage;
}
async function prepareRetrievalResultsContextInjection(ctl, originalUserPrompt, files) {
  const pluginConfig = ctl.getPluginConfig(configSchematics);
  const retrievalLimit = pluginConfig.get("retrievalLimit");
  const retrievalAffinityThreshold = pluginConfig.get("retrievalAffinityThreshold");
  const statusSteps = /* @__PURE__ */ new Map();
  const retrievingStatus = ctl.createStatus({
    status: "loading",
    text: `Loading an embedding model for retrieval...`
  });
  const model = await ctl.client.embedding.model("nomic-ai/nomic-embed-text-v1.5-GGUF", {
    signal: ctl.abortSignal
  });
  retrievingStatus.setState({
    status: "loading",
    text: `Retrieving relevant citations for user query...`
  });
  const result = await ctl.client.files.retrieve(originalUserPrompt, files, {
    embeddingModel: model,
    // Affinity threshold: 0.6 not implemented
    limit: retrievalLimit,
    signal: ctl.abortSignal,
    onFileProcessList(filesToProcess) {
      for (const file of filesToProcess) {
        statusSteps.set(
          file,
          retrievingStatus.addSubStatus({
            status: "waiting",
            text: `Process ${file.name} for retrieval`
          })
        );
      }
    },
    onFileProcessingStart(file) {
      statusSteps.get(file).setState({ status: "loading", text: `Processing ${file.name} for retrieval` });
    },
    onFileProcessingEnd(file) {
      statusSteps.get(file).setState({ status: "done", text: `Processed ${file.name} for retrieval` });
    },
    onFileProcessingStepProgress(file, step, progressInStep) {
      const verb = step === "loading" ? "Loading" : step === "chunking" ? "Chunking" : "Embedding";
      statusSteps.get(file).setState({
        status: "loading",
        text: `${verb} ${file.name} for retrieval (${(progressInStep * 100).toFixed(1)}%)`
      });
    }
  });
  result.entries = result.entries.filter((entry) => entry.score > retrievalAffinityThreshold);
  let processedContent = "";
  const numRetrievals = result.entries.length;
  if (numRetrievals > 0) {
    retrievingStatus.setState({
      status: "done",
      text: `Retrieved ${numRetrievals} relevant citations for user query`
    });
    ctl.debug("Retrieval results", result);
    const prefix = "The following citations were found in the files provided by the user:\n\n";
    processedContent += prefix;
    let citationNumber = 1;
    result.entries.forEach((result2) => {
      const completeText = result2.content;
      processedContent += `Citation ${citationNumber}: "${completeText}"

`;
      citationNumber++;
    });
    await ctl.addCitations(result);
    const suffix = `Use the citations above to respond to the user query, only if they are relevant. Otherwise, respond to the best of your ability without them.

User Query:

${originalUserPrompt}`;
    processedContent += suffix;
  } else {
    retrievingStatus.setState({
      status: "canceled",
      text: `No relevant citations found for user query`
    });
    ctl.debug("No relevant citations found for user query");
    const noteAboutNoRetrievalResultsFound = `Important: No citations were found in the user files for the user query. In less than one sentence, inform the user of this. Then respond to the query to the best of your ability.`;
    processedContent = noteAboutNoRetrievalResultsFound + `

User Query:

${originalUserPrompt}`;
  }
  ctl.debug("Processed content", processedContent);
  return processedContent;
}
async function prepareDocumentContextInjection(ctl, input) {
  const documentInjectionSnippets = /* @__PURE__ */ new Map();
  const files = input.consumeFiles(ctl.client, (file) => file.type !== "image");
  for (const file of files) {
    const { content } = await ctl.client.files.parseDocument(file, {
      signal: ctl.abortSignal
    });
    ctl.debug(import_sdk2.text`
      Strategy: inject-full-content. Injecting full content of file '${file}' into the
      context. Length: ${content.length}.
    `);
    documentInjectionSnippets.set(file, content);
  }
  let formattedFinalUserPrompt = "";
  if (documentInjectionSnippets.size > 0) {
    formattedFinalUserPrompt += "This is a Enriched Context Generation scenario.\n\nThe following content was found in the files provided by the user.\n";
    for (const [fileHandle, snippet] of documentInjectionSnippets) {
      formattedFinalUserPrompt += `

** ${fileHandle.name} full content **

${snippet}

** end of ${fileHandle.name} **

`;
    }
    formattedFinalUserPrompt += `Based on the content above, please provide a response to the user query.

User query: ${input.getText()}`;
  }
  input.replaceText(formattedFinalUserPrompt);
  return input;
}
async function measureContextWindow(ctx, model) {
  const currentContextFormatted = await model.applyPromptTemplate(ctx);
  const totalTokensInContext = await model.countTokens(currentContextFormatted);
  const modelContextLength = await model.getContextLength();
  const modelRemainingContextLength = modelContextLength - totalTokensInContext;
  const contextOccupiedPercent = totalTokensInContext / modelContextLength * 100;
  return {
    totalTokensInContext,
    modelContextLength,
    modelRemainingContextLength,
    contextOccupiedPercent
  };
}
async function chooseContextInjectionStrategy(ctl, originalUserPrompt, files) {
  const status = ctl.createStatus({
    status: "loading",
    text: `Deciding how to handle the document(s)...`
  });
  const model = await ctl.client.llm.model();
  const ctx = await ctl.pullHistory();
  const {
    totalTokensInContext,
    modelContextLength,
    modelRemainingContextLength,
    contextOccupiedPercent
  } = await measureContextWindow(ctx, model);
  ctl.debug(
    `Context measurement result:

	Total tokens in context: ${totalTokensInContext}
	Model context length: ${modelContextLength}
	Model remaining context length: ${modelRemainingContextLength}
	Context occupied percent: ${contextOccupiedPercent.toFixed(2)}%
`
  );
  let totalFileTokenCount = 0;
  let totalReadTime = 0;
  let totalTokenizeTime = 0;
  for (const file of files) {
    const startTime = performance.now();
    const loadingStatus = status.addSubStatus({
      status: "loading",
      text: `Loading parser for ${file.name}...`
    });
    let actionProgressing = "Reading";
    let parserIndicator = "";
    const { content } = await ctl.client.files.parseDocument(file, {
      signal: ctl.abortSignal,
      onParserLoaded: (parser) => {
        loadingStatus.setState({
          status: "loading",
          text: `${parser.library} loaded for ${file.name}...`
        });
        if (parser.library !== "builtIn") {
          actionProgressing = "Parsing";
          parserIndicator = ` with ${parser.library}`;
        }
      },
      onProgress: (progress) => {
        loadingStatus.setState({
          status: "loading",
          text: `${actionProgressing} file ${file.name}${parserIndicator}... (${(progress * 100).toFixed(2)}%)`
        });
      }
    });
    loadingStatus.remove();
    totalReadTime += performance.now() - startTime;
    const startTokenizeTime = performance.now();
    totalFileTokenCount += await model.countTokens(content);
    totalTokenizeTime += performance.now() - startTokenizeTime;
    if (totalFileTokenCount > modelRemainingContextLength) {
      break;
    }
  }
  ctl.debug(`Total file read time: ${totalReadTime.toFixed(2)} ms`);
  ctl.debug(`Total tokenize time: ${totalTokenizeTime.toFixed(2)} ms`);
  ctl.debug(`Original User Prompt: ${originalUserPrompt}`);
  const userPromptTokenCount = (await model.tokenize(originalUserPrompt)).length;
  const totalFilePlusPromptTokenCount = totalFileTokenCount + userPromptTokenCount;
  const contextOccupiedFraction = contextOccupiedPercent / 100;
  const targetContextUsePercent = 0.7;
  const targetContextUsage = targetContextUsePercent * (1 - contextOccupiedFraction);
  const availableContextTokens = Math.floor(modelRemainingContextLength * targetContextUsage);
  ctl.debug("Strategy Calculation:");
  ctl.debug(`	Total Tokens in All Files: ${totalFileTokenCount}`);
  ctl.debug(`	Total Tokens in User Prompt: ${userPromptTokenCount}`);
  ctl.debug(`	Model Context Remaining: ${modelRemainingContextLength} tokens`);
  ctl.debug(`	Context Occupied: ${contextOccupiedPercent.toFixed(2)}%`);
  ctl.debug(`	Available Tokens: ${availableContextTokens}
`);
  if (totalFilePlusPromptTokenCount > availableContextTokens) {
    const chosenStrategy2 = "retrieval";
    ctl.debug(
      `Chosen context injection strategy: '${chosenStrategy2}'. Total file + prompt token count: ${totalFilePlusPromptTokenCount} > ${targetContextUsage * 100}% * available context tokens: ${availableContextTokens}`
    );
    status.setState({
      status: "done",
      text: `Chosen context injection strategy: '${chosenStrategy2}'. Retrieval is optimal for the size of content provided`
    });
    return chosenStrategy2;
  }
  const chosenStrategy = "inject-full-content";
  status.setState({
    status: "done",
    text: `Chosen context injection strategy: '${chosenStrategy}'. All content can fit into the context`
  });
  return chosenStrategy;
}
var import_sdk2;
var init_promptPreprocessor = __esm({
  "C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/src/promptPreprocessor.ts"() {
    "use strict";
    import_sdk2 = require("@lmstudio/sdk");
    init_config();
  }
});

// C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/src/index.ts
var src_exports = {};
__export(src_exports, {
  main: () => main
});
async function main(context) {
  context.withConfigSchematics(configSchematics);
  context.withPromptPreprocessor(preprocess);
}
var init_src = __esm({
  "C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/src/index.ts"() {
    "use strict";
    init_config();
    init_promptPreprocessor();
  }
});

// C:/Users/RUNNER~1/AppData/Local/Temp/4141abd037436b1b7d6d2816622965c1/.lmstudio/entry.ts
var import_sdk3 = require("@lmstudio/sdk");
var clientIdentifier = process.env.LMS_PLUGIN_CLIENT_IDENTIFIER;
var clientPasskey = process.env.LMS_PLUGIN_CLIENT_PASSKEY;
var baseUrl = process.env.LMS_PLUGIN_BASE_URL;
var client = new import_sdk3.LMStudioClient({
  clientIdentifier,
  clientPasskey,
  baseUrl
});
globalThis.__LMS_PLUGIN_CONTEXT = true;
var predictionLoopHandlerSet = false;
var promptPreprocessorSet = false;
var configSchematicsSet = false;
var globalConfigSchematicsSet = false;
var toolsProviderSet = false;
var generatorSet = false;
var selfRegistrationHost = client.plugins.getSelfRegistrationHost();
var pluginContext = {
  withPredictionLoopHandler: (generate) => {
    if (predictionLoopHandlerSet) {
      throw new Error("PredictionLoopHandler already registered");
    }
    if (toolsProviderSet) {
      throw new Error("PredictionLoopHandler cannot be used with a tools provider");
    }
    predictionLoopHandlerSet = true;
    selfRegistrationHost.setPredictionLoopHandler(generate);
    return pluginContext;
  },
  withPromptPreprocessor: (preprocess2) => {
    if (promptPreprocessorSet) {
      throw new Error("PromptPreprocessor already registered");
    }
    promptPreprocessorSet = true;
    selfRegistrationHost.setPromptPreprocessor(preprocess2);
    return pluginContext;
  },
  withConfigSchematics: (configSchematics2) => {
    if (configSchematicsSet) {
      throw new Error("Config schematics already registered");
    }
    configSchematicsSet = true;
    selfRegistrationHost.setConfigSchematics(configSchematics2);
    return pluginContext;
  },
  withGlobalConfigSchematics: (globalConfigSchematics) => {
    if (globalConfigSchematicsSet) {
      throw new Error("Global config schematics already registered");
    }
    globalConfigSchematicsSet = true;
    selfRegistrationHost.setGlobalConfigSchematics(globalConfigSchematics);
    return pluginContext;
  },
  withToolsProvider: (toolsProvider) => {
    if (toolsProviderSet) {
      throw new Error("Tools provider already registered");
    }
    if (predictionLoopHandlerSet) {
      throw new Error("Tools provider cannot be used with a predictionLoopHandler");
    }
    toolsProviderSet = true;
    selfRegistrationHost.setToolsProvider(toolsProvider);
    return pluginContext;
  },
  withGenerator: (generator) => {
    if (generatorSet) {
      throw new Error("Generator already registered");
    }
    generatorSet = true;
    selfRegistrationHost.setGenerator(generator);
    return pluginContext;
  }
};
Promise.resolve().then(() => (init_src(), src_exports)).then(async (module2) => {
  return await module2.main(pluginContext);
}).then(() => {
  selfRegistrationHost.initCompleted();
}).catch((error) => {
  console.error("Failed to execute the main function of the plugin.");
  console.error(error);
});
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsiLi4vc3JjL2NvbmZpZy50cyIsICIuLi9zcmMvcHJvbXB0UHJlcHJvY2Vzc29yLnRzIiwgIi4uL3NyYy9pbmRleC50cyIsICJlbnRyeS50cyJdLAogICJzb3VyY2VzQ29udGVudCI6IFsiaW1wb3J0IHsgY3JlYXRlQ29uZmlnU2NoZW1hdGljcyB9IGZyb20gXCJAbG1zdHVkaW8vc2RrXCI7XHJcblxyXG5leHBvcnQgY29uc3QgY29uZmlnU2NoZW1hdGljcyA9IGNyZWF0ZUNvbmZpZ1NjaGVtYXRpY3MoKVxyXG4gIC5maWVsZChcclxuICAgIFwicmV0cmlldmFsTGltaXRcIixcclxuICAgIFwibnVtZXJpY1wiLFxyXG4gICAge1xyXG4gICAgICBpbnQ6IHRydWUsXHJcbiAgICAgIG1pbjogMSxcclxuICAgICAgZGlzcGxheU5hbWU6IFwiUmV0cmlldmFsIExpbWl0XCIsXHJcbiAgICAgIHN1YnRpdGxlOiBcIldoZW4gcmV0cmlldmFsIGlzIHRyaWdnZXJlZCwgdGhpcyBpcyB0aGUgbWF4aW11bSBudW1iZXIgb2YgY2h1bmtzIHRvIHJldHVybi5cIixcclxuICAgICAgc2xpZGVyOiB7IG1pbjogMSwgbWF4OiAxMCwgc3RlcDogMSB9LFxyXG4gICAgfSxcclxuICAgIDMsXHJcbiAgKVxyXG4gIC5maWVsZChcclxuICAgIFwicmV0cmlldmFsQWZmaW5pdHlUaHJlc2hvbGRcIixcclxuICAgIFwibnVtZXJpY1wiLFxyXG4gICAge1xyXG4gICAgICBtaW46IDAuMCxcclxuICAgICAgbWF4OiAxLjAsXHJcbiAgICAgIGRpc3BsYXlOYW1lOiBcIlJldHJpZXZhbCBBZmZpbml0eSBUaHJlc2hvbGRcIixcclxuICAgICAgc3VidGl0bGU6IFwiVGhlIG1pbmltdW0gc2ltaWxhcml0eSBzY29yZSBmb3IgYSBjaHVuayB0byBiZSBjb25zaWRlcmVkIHJlbGV2YW50LlwiLFxyXG4gICAgICBzbGlkZXI6IHsgbWluOiAwLjAsIG1heDogMS4wLCBzdGVwOiAwLjAxIH0sXHJcbiAgICB9LFxyXG4gICAgMC41LFxyXG4gIClcclxuICAuYnVpbGQoKTtcclxuIiwgImltcG9ydCB7XHJcbiAgdGV4dCxcclxuICB0eXBlIENoYXQsXHJcbiAgdHlwZSBDaGF0TWVzc2FnZSxcclxuICB0eXBlIEZpbGVIYW5kbGUsXHJcbiAgdHlwZSBMTE1EeW5hbWljSGFuZGxlLFxyXG4gIHR5cGUgUHJlZGljdGlvblByb2Nlc3NTdGF0dXNDb250cm9sbGVyLFxyXG4gIHR5cGUgUHJvbXB0UHJlcHJvY2Vzc29yQ29udHJvbGxlcixcclxufSBmcm9tIFwiQGxtc3R1ZGlvL3Nka1wiO1xyXG5pbXBvcnQgeyBjb25maWdTY2hlbWF0aWNzIH0gZnJvbSBcIi4vY29uZmlnXCI7XHJcblxyXG50eXBlIERvY3VtZW50Q29udGV4dEluamVjdGlvblN0cmF0ZWd5ID0gXCJub25lXCIgfCBcImluamVjdC1mdWxsLWNvbnRlbnRcIiB8IFwicmV0cmlldmFsXCI7XHJcblxyXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gcHJlcHJvY2VzcyhjdGw6IFByb21wdFByZXByb2Nlc3NvckNvbnRyb2xsZXIsIHVzZXJNZXNzYWdlOiBDaGF0TWVzc2FnZSkge1xyXG4gIGNvbnN0IHVzZXJQcm9tcHQgPSB1c2VyTWVzc2FnZS5nZXRUZXh0KCk7XHJcbiAgY29uc3QgaGlzdG9yeSA9IGF3YWl0IGN0bC5wdWxsSGlzdG9yeSgpO1xyXG4gIGhpc3RvcnkuYXBwZW5kKHVzZXJNZXNzYWdlKTtcclxuICBjb25zdCBuZXdGaWxlcyA9IHVzZXJNZXNzYWdlLmdldEZpbGVzKGN0bC5jbGllbnQpLmZpbHRlcihmID0+IGYudHlwZSAhPT0gXCJpbWFnZVwiKTtcclxuICBjb25zdCBmaWxlcyA9IGhpc3RvcnkuZ2V0QWxsRmlsZXMoY3RsLmNsaWVudCkuZmlsdGVyKGYgPT4gZi50eXBlICE9PSBcImltYWdlXCIpO1xyXG5cclxuICBpZiAobmV3RmlsZXMubGVuZ3RoID4gMCkge1xyXG4gICAgY29uc3Qgc3RyYXRlZ3kgPSBhd2FpdCBjaG9vc2VDb250ZXh0SW5qZWN0aW9uU3RyYXRlZ3koY3RsLCB1c2VyUHJvbXB0LCBuZXdGaWxlcyk7XHJcbiAgICBpZiAoc3RyYXRlZ3kgPT09IFwiaW5qZWN0LWZ1bGwtY29udGVudFwiKSB7XHJcbiAgICAgIHJldHVybiBhd2FpdCBwcmVwYXJlRG9jdW1lbnRDb250ZXh0SW5qZWN0aW9uKGN0bCwgdXNlck1lc3NhZ2UpO1xyXG4gICAgfSBlbHNlIGlmIChzdHJhdGVneSA9PT0gXCJyZXRyaWV2YWxcIikge1xyXG4gICAgICByZXR1cm4gYXdhaXQgcHJlcGFyZVJldHJpZXZhbFJlc3VsdHNDb250ZXh0SW5qZWN0aW9uKGN0bCwgdXNlclByb21wdCwgZmlsZXMpO1xyXG4gICAgfVxyXG4gIH0gZWxzZSBpZiAoZmlsZXMubGVuZ3RoID4gMCkge1xyXG4gICAgcmV0dXJuIGF3YWl0IHByZXBhcmVSZXRyaWV2YWxSZXN1bHRzQ29udGV4dEluamVjdGlvbihjdGwsIHVzZXJQcm9tcHQsIGZpbGVzKTtcclxuICB9XHJcblxyXG4gIHJldHVybiB1c2VyTWVzc2FnZTtcclxufVxyXG5cclxuYXN5bmMgZnVuY3Rpb24gcHJlcGFyZVJldHJpZXZhbFJlc3VsdHNDb250ZXh0SW5qZWN0aW9uKFxyXG4gIGN0bDogUHJvbXB0UHJlcHJvY2Vzc29yQ29udHJvbGxlcixcclxuICBvcmlnaW5hbFVzZXJQcm9tcHQ6IHN0cmluZyxcclxuICBmaWxlczogQXJyYXk8RmlsZUhhbmRsZT4sXHJcbik6IFByb21pc2U8c3RyaW5nPiB7XHJcbiAgY29uc3QgcGx1Z2luQ29uZmlnID0gY3RsLmdldFBsdWdpbkNvbmZpZyhjb25maWdTY2hlbWF0aWNzKTtcclxuICBjb25zdCByZXRyaWV2YWxMaW1pdCA9IHBsdWdpbkNvbmZpZy5nZXQoXCJyZXRyaWV2YWxMaW1pdFwiKTtcclxuICBjb25zdCByZXRyaWV2YWxBZmZpbml0eVRocmVzaG9sZCA9IHBsdWdpbkNvbmZpZy5nZXQoXCJyZXRyaWV2YWxBZmZpbml0eVRocmVzaG9sZFwiKTtcclxuXHJcbiAgLy8gcHJvY2VzcyBmaWxlcyBpZiBuZWNlc3NhcnlcclxuXHJcbiAgY29uc3Qgc3RhdHVzU3RlcHMgPSBuZXcgTWFwPEZpbGVIYW5kbGUsIFByZWRpY3Rpb25Qcm9jZXNzU3RhdHVzQ29udHJvbGxlcj4oKTtcclxuXHJcbiAgY29uc3QgcmV0cmlldmluZ1N0YXR1cyA9IGN0bC5jcmVhdGVTdGF0dXMoe1xyXG4gICAgc3RhdHVzOiBcImxvYWRpbmdcIixcclxuICAgIHRleHQ6IGBMb2FkaW5nIGFuIGVtYmVkZGluZyBtb2RlbCBmb3IgcmV0cmlldmFsLi4uYCxcclxuICB9KTtcclxuICBjb25zdCBtb2RlbCA9IGF3YWl0IGN0bC5jbGllbnQuZW1iZWRkaW5nLm1vZGVsKFwibm9taWMtYWkvbm9taWMtZW1iZWQtdGV4dC12MS41LUdHVUZcIiwge1xyXG4gICAgc2lnbmFsOiBjdGwuYWJvcnRTaWduYWwsXHJcbiAgfSk7XHJcbiAgcmV0cmlldmluZ1N0YXR1cy5zZXRTdGF0ZSh7XHJcbiAgICBzdGF0dXM6IFwibG9hZGluZ1wiLFxyXG4gICAgdGV4dDogYFJldHJpZXZpbmcgcmVsZXZhbnQgY2l0YXRpb25zIGZvciB1c2VyIHF1ZXJ5Li4uYCxcclxuICB9KTtcclxuICBjb25zdCByZXN1bHQgPSBhd2FpdCBjdGwuY2xpZW50LmZpbGVzLnJldHJpZXZlKG9yaWdpbmFsVXNlclByb21wdCwgZmlsZXMsIHtcclxuICAgIGVtYmVkZGluZ01vZGVsOiBtb2RlbCxcclxuICAgIC8vIEFmZmluaXR5IHRocmVzaG9sZDogMC42IG5vdCBpbXBsZW1lbnRlZFxyXG4gICAgbGltaXQ6IHJldHJpZXZhbExpbWl0LFxyXG4gICAgc2lnbmFsOiBjdGwuYWJvcnRTaWduYWwsXHJcbiAgICBvbkZpbGVQcm9jZXNzTGlzdChmaWxlc1RvUHJvY2Vzcykge1xyXG4gICAgICBmb3IgKGNvbnN0IGZpbGUgb2YgZmlsZXNUb1Byb2Nlc3MpIHtcclxuICAgICAgICBzdGF0dXNTdGVwcy5zZXQoXHJcbiAgICAgICAgICBmaWxlLFxyXG4gICAgICAgICAgcmV0cmlldmluZ1N0YXR1cy5hZGRTdWJTdGF0dXMoe1xyXG4gICAgICAgICAgICBzdGF0dXM6IFwid2FpdGluZ1wiLFxyXG4gICAgICAgICAgICB0ZXh0OiBgUHJvY2VzcyAke2ZpbGUubmFtZX0gZm9yIHJldHJpZXZhbGAsXHJcbiAgICAgICAgICB9KSxcclxuICAgICAgICApO1xyXG4gICAgICB9XHJcbiAgICB9LFxyXG4gICAgb25GaWxlUHJvY2Vzc2luZ1N0YXJ0KGZpbGUpIHtcclxuICAgICAgc3RhdHVzU3RlcHNcclxuICAgICAgICAuZ2V0KGZpbGUpIVxyXG4gICAgICAgIC5zZXRTdGF0ZSh7IHN0YXR1czogXCJsb2FkaW5nXCIsIHRleHQ6IGBQcm9jZXNzaW5nICR7ZmlsZS5uYW1lfSBmb3IgcmV0cmlldmFsYCB9KTtcclxuICAgIH0sXHJcbiAgICBvbkZpbGVQcm9jZXNzaW5nRW5kKGZpbGUpIHtcclxuICAgICAgc3RhdHVzU3RlcHNcclxuICAgICAgICAuZ2V0KGZpbGUpIVxyXG4gICAgICAgIC5zZXRTdGF0ZSh7IHN0YXR1czogXCJkb25lXCIsIHRleHQ6IGBQcm9jZXNzZWQgJHtmaWxlLm5hbWV9IGZvciByZXRyaWV2YWxgIH0pO1xyXG4gICAgfSxcclxuICAgIG9uRmlsZVByb2Nlc3NpbmdTdGVwUHJvZ3Jlc3MoZmlsZSwgc3RlcCwgcHJvZ3Jlc3NJblN0ZXApIHtcclxuICAgICAgY29uc3QgdmVyYiA9IHN0ZXAgPT09IFwibG9hZGluZ1wiID8gXCJMb2FkaW5nXCIgOiBzdGVwID09PSBcImNodW5raW5nXCIgPyBcIkNodW5raW5nXCIgOiBcIkVtYmVkZGluZ1wiO1xyXG4gICAgICBzdGF0dXNTdGVwcy5nZXQoZmlsZSkhLnNldFN0YXRlKHtcclxuICAgICAgICBzdGF0dXM6IFwibG9hZGluZ1wiLFxyXG4gICAgICAgIHRleHQ6IGAke3ZlcmJ9ICR7ZmlsZS5uYW1lfSBmb3IgcmV0cmlldmFsICgkeyhwcm9ncmVzc0luU3RlcCAqIDEwMCkudG9GaXhlZCgxKX0lKWAsXHJcbiAgICAgIH0pO1xyXG4gICAgfSxcclxuICB9KTtcclxuXHJcbiAgcmVzdWx0LmVudHJpZXMgPSByZXN1bHQuZW50cmllcy5maWx0ZXIoZW50cnkgPT4gZW50cnkuc2NvcmUgPiByZXRyaWV2YWxBZmZpbml0eVRocmVzaG9sZCk7XHJcblxyXG4gIC8vIGluamVjdCByZXRyaWV2YWwgcmVzdWx0IGludG8gdGhlIFwicHJvY2Vzc2VkXCIgY29udGVudFxyXG4gIGxldCBwcm9jZXNzZWRDb250ZW50ID0gXCJcIjtcclxuICBjb25zdCBudW1SZXRyaWV2YWxzID0gcmVzdWx0LmVudHJpZXMubGVuZ3RoO1xyXG4gIGlmIChudW1SZXRyaWV2YWxzID4gMCkge1xyXG4gICAgLy8gcmV0cmlldmFsIG9jY3VyZWQgYW5kIGdvdCByZXN1bHRzXHJcbiAgICAvLyBzaG93IHN0YXR1c1xyXG4gICAgcmV0cmlldmluZ1N0YXR1cy5zZXRTdGF0ZSh7XHJcbiAgICAgIHN0YXR1czogXCJkb25lXCIsXHJcbiAgICAgIHRleHQ6IGBSZXRyaWV2ZWQgJHtudW1SZXRyaWV2YWxzfSByZWxldmFudCBjaXRhdGlvbnMgZm9yIHVzZXIgcXVlcnlgLFxyXG4gICAgfSk7XHJcbiAgICBjdGwuZGVidWcoXCJSZXRyaWV2YWwgcmVzdWx0c1wiLCByZXN1bHQpO1xyXG4gICAgLy8gYWRkIHJlc3VsdHMgdG8gcHJvbXB0XHJcbiAgICBjb25zdCBwcmVmaXggPSBcIlRoZSBmb2xsb3dpbmcgY2l0YXRpb25zIHdlcmUgZm91bmQgaW4gdGhlIGZpbGVzIHByb3ZpZGVkIGJ5IHRoZSB1c2VyOlxcblxcblwiO1xyXG4gICAgcHJvY2Vzc2VkQ29udGVudCArPSBwcmVmaXg7XHJcbiAgICBsZXQgY2l0YXRpb25OdW1iZXIgPSAxO1xyXG4gICAgcmVzdWx0LmVudHJpZXMuZm9yRWFjaChyZXN1bHQgPT4ge1xyXG4gICAgICBjb25zdCBjb21wbGV0ZVRleHQgPSByZXN1bHQuY29udGVudDtcclxuICAgICAgcHJvY2Vzc2VkQ29udGVudCArPSBgQ2l0YXRpb24gJHtjaXRhdGlvbk51bWJlcn06IFwiJHtjb21wbGV0ZVRleHR9XCJcXG5cXG5gO1xyXG4gICAgICBjaXRhdGlvbk51bWJlcisrO1xyXG4gICAgfSk7XHJcbiAgICBhd2FpdCBjdGwuYWRkQ2l0YXRpb25zKHJlc3VsdCk7XHJcbiAgICBjb25zdCBzdWZmaXggPVxyXG4gICAgICBgVXNlIHRoZSBjaXRhdGlvbnMgYWJvdmUgdG8gcmVzcG9uZCB0byB0aGUgdXNlciBxdWVyeSwgb25seSBpZiB0aGV5IGFyZSByZWxldmFudC4gYCArXHJcbiAgICAgIGBPdGhlcndpc2UsIHJlc3BvbmQgdG8gdGhlIGJlc3Qgb2YgeW91ciBhYmlsaXR5IHdpdGhvdXQgdGhlbS5gICtcclxuICAgICAgYFxcblxcblVzZXIgUXVlcnk6XFxuXFxuJHtvcmlnaW5hbFVzZXJQcm9tcHR9YDtcclxuICAgIHByb2Nlc3NlZENvbnRlbnQgKz0gc3VmZml4O1xyXG4gIH0gZWxzZSB7XHJcbiAgICAvLyByZXRyaWV2YWwgb2NjdXJlZCBidXQgbm8gcmVsZXZhbnQgY2l0YXRpb25zIGZvdW5kXHJcbiAgICByZXRyaWV2aW5nU3RhdHVzLnNldFN0YXRlKHtcclxuICAgICAgc3RhdHVzOiBcImNhbmNlbGVkXCIsXHJcbiAgICAgIHRleHQ6IGBObyByZWxldmFudCBjaXRhdGlvbnMgZm91bmQgZm9yIHVzZXIgcXVlcnlgLFxyXG4gICAgfSk7XHJcbiAgICBjdGwuZGVidWcoXCJObyByZWxldmFudCBjaXRhdGlvbnMgZm91bmQgZm9yIHVzZXIgcXVlcnlcIik7XHJcbiAgICBjb25zdCBub3RlQWJvdXROb1JldHJpZXZhbFJlc3VsdHNGb3VuZCA9XHJcbiAgICAgIGBJbXBvcnRhbnQ6IE5vIGNpdGF0aW9ucyB3ZXJlIGZvdW5kIGluIHRoZSB1c2VyIGZpbGVzIGZvciB0aGUgdXNlciBxdWVyeS4gYCArXHJcbiAgICAgIGBJbiBsZXNzIHRoYW4gb25lIHNlbnRlbmNlLCBpbmZvcm0gdGhlIHVzZXIgb2YgdGhpcy4gYCArXHJcbiAgICAgIGBUaGVuIHJlc3BvbmQgdG8gdGhlIHF1ZXJ5IHRvIHRoZSBiZXN0IG9mIHlvdXIgYWJpbGl0eS5gO1xyXG4gICAgcHJvY2Vzc2VkQ29udGVudCA9XHJcbiAgICAgIG5vdGVBYm91dE5vUmV0cmlldmFsUmVzdWx0c0ZvdW5kICsgYFxcblxcblVzZXIgUXVlcnk6XFxuXFxuJHtvcmlnaW5hbFVzZXJQcm9tcHR9YDtcclxuICB9XHJcbiAgY3RsLmRlYnVnKFwiUHJvY2Vzc2VkIGNvbnRlbnRcIiwgcHJvY2Vzc2VkQ29udGVudCk7XHJcblxyXG4gIHJldHVybiBwcm9jZXNzZWRDb250ZW50O1xyXG59XHJcblxyXG5hc3luYyBmdW5jdGlvbiBwcmVwYXJlRG9jdW1lbnRDb250ZXh0SW5qZWN0aW9uKFxyXG4gIGN0bDogUHJvbXB0UHJlcHJvY2Vzc29yQ29udHJvbGxlcixcclxuICBpbnB1dDogQ2hhdE1lc3NhZ2UsXHJcbik6IFByb21pc2U8Q2hhdE1lc3NhZ2U+IHtcclxuICBjb25zdCBkb2N1bWVudEluamVjdGlvblNuaXBwZXRzOiBNYXA8RmlsZUhhbmRsZSwgc3RyaW5nPiA9IG5ldyBNYXAoKTtcclxuICBjb25zdCBmaWxlcyA9IGlucHV0LmNvbnN1bWVGaWxlcyhjdGwuY2xpZW50LCBmaWxlID0+IGZpbGUudHlwZSAhPT0gXCJpbWFnZVwiKTtcclxuICBmb3IgKGNvbnN0IGZpbGUgb2YgZmlsZXMpIHtcclxuICAgIC8vIFRoaXMgc2hvdWxkIHRha2Ugbm8gdGltZSBhcyB0aGUgcmVzdWx0IGlzIGFscmVhZHkgaW4gdGhlIGNhY2hlXHJcbiAgICBjb25zdCB7IGNvbnRlbnQgfSA9IGF3YWl0IGN0bC5jbGllbnQuZmlsZXMucGFyc2VEb2N1bWVudChmaWxlLCB7XHJcbiAgICAgIHNpZ25hbDogY3RsLmFib3J0U2lnbmFsLFxyXG4gICAgfSk7XHJcblxyXG4gICAgY3RsLmRlYnVnKHRleHRgXHJcbiAgICAgIFN0cmF0ZWd5OiBpbmplY3QtZnVsbC1jb250ZW50LiBJbmplY3RpbmcgZnVsbCBjb250ZW50IG9mIGZpbGUgJyR7ZmlsZX0nIGludG8gdGhlXHJcbiAgICAgIGNvbnRleHQuIExlbmd0aDogJHtjb250ZW50Lmxlbmd0aH0uXHJcbiAgICBgKTtcclxuICAgIGRvY3VtZW50SW5qZWN0aW9uU25pcHBldHMuc2V0KGZpbGUsIGNvbnRlbnQpO1xyXG4gIH1cclxuXHJcbiAgLy8gRm9ybWF0IHRoZSBmaW5hbCB1c2VyIHByb21wdFxyXG4gIC8vIFRPRE86XHJcbiAgLy8gICAgTWFrZSB0aGlzIHRlbXBsYXRhYmxlIGFuZCBjb25maWd1cmFibGVcclxuICAvLyAgICAgIGh0dHBzOi8vZ2l0aHViLmNvbS9sbXN0dWRpby1haS9sbG1zdGVyL2lzc3Vlcy8xMDE3XHJcbiAgbGV0IGZvcm1hdHRlZEZpbmFsVXNlclByb21wdCA9IFwiXCI7XHJcblxyXG4gIGlmIChkb2N1bWVudEluamVjdGlvblNuaXBwZXRzLnNpemUgPiAwKSB7XHJcbiAgICBmb3JtYXR0ZWRGaW5hbFVzZXJQcm9tcHQgKz1cclxuICAgICAgXCJUaGlzIGlzIGEgRW5yaWNoZWQgQ29udGV4dCBHZW5lcmF0aW9uIHNjZW5hcmlvLlxcblxcblRoZSBmb2xsb3dpbmcgY29udGVudCB3YXMgZm91bmQgaW4gdGhlIGZpbGVzIHByb3ZpZGVkIGJ5IHRoZSB1c2VyLlxcblwiO1xyXG5cclxuICAgIGZvciAoY29uc3QgW2ZpbGVIYW5kbGUsIHNuaXBwZXRdIG9mIGRvY3VtZW50SW5qZWN0aW9uU25pcHBldHMpIHtcclxuICAgICAgZm9ybWF0dGVkRmluYWxVc2VyUHJvbXB0ICs9IGBcXG5cXG4qKiAke2ZpbGVIYW5kbGUubmFtZX0gZnVsbCBjb250ZW50ICoqXFxuXFxuJHtzbmlwcGV0fVxcblxcbioqIGVuZCBvZiAke2ZpbGVIYW5kbGUubmFtZX0gKipcXG5cXG5gO1xyXG4gICAgfVxyXG5cclxuICAgIGZvcm1hdHRlZEZpbmFsVXNlclByb21wdCArPSBgQmFzZWQgb24gdGhlIGNvbnRlbnQgYWJvdmUsIHBsZWFzZSBwcm92aWRlIGEgcmVzcG9uc2UgdG8gdGhlIHVzZXIgcXVlcnkuXFxuXFxuVXNlciBxdWVyeTogJHtpbnB1dC5nZXRUZXh0KCl9YDtcclxuICB9XHJcblxyXG4gIGlucHV0LnJlcGxhY2VUZXh0KGZvcm1hdHRlZEZpbmFsVXNlclByb21wdCk7XHJcbiAgcmV0dXJuIGlucHV0O1xyXG59XHJcblxyXG5hc3luYyBmdW5jdGlvbiBtZWFzdXJlQ29udGV4dFdpbmRvdyhjdHg6IENoYXQsIG1vZGVsOiBMTE1EeW5hbWljSGFuZGxlKSB7XHJcbiAgY29uc3QgY3VycmVudENvbnRleHRGb3JtYXR0ZWQgPSBhd2FpdCBtb2RlbC5hcHBseVByb21wdFRlbXBsYXRlKGN0eCk7XHJcbiAgY29uc3QgdG90YWxUb2tlbnNJbkNvbnRleHQgPSBhd2FpdCBtb2RlbC5jb3VudFRva2VucyhjdXJyZW50Q29udGV4dEZvcm1hdHRlZCk7XHJcbiAgY29uc3QgbW9kZWxDb250ZXh0TGVuZ3RoID0gYXdhaXQgbW9kZWwuZ2V0Q29udGV4dExlbmd0aCgpO1xyXG4gIGNvbnN0IG1vZGVsUmVtYWluaW5nQ29udGV4dExlbmd0aCA9IG1vZGVsQ29udGV4dExlbmd0aCAtIHRvdGFsVG9rZW5zSW5Db250ZXh0O1xyXG4gIGNvbnN0IGNvbnRleHRPY2N1cGllZFBlcmNlbnQgPSAodG90YWxUb2tlbnNJbkNvbnRleHQgLyBtb2RlbENvbnRleHRMZW5ndGgpICogMTAwO1xyXG4gIHJldHVybiB7XHJcbiAgICB0b3RhbFRva2Vuc0luQ29udGV4dCxcclxuICAgIG1vZGVsQ29udGV4dExlbmd0aCxcclxuICAgIG1vZGVsUmVtYWluaW5nQ29udGV4dExlbmd0aCxcclxuICAgIGNvbnRleHRPY2N1cGllZFBlcmNlbnQsXHJcbiAgfTtcclxufVxyXG5cclxuYXN5bmMgZnVuY3Rpb24gY2hvb3NlQ29udGV4dEluamVjdGlvblN0cmF0ZWd5KFxyXG4gIGN0bDogUHJvbXB0UHJlcHJvY2Vzc29yQ29udHJvbGxlcixcclxuICBvcmlnaW5hbFVzZXJQcm9tcHQ6IHN0cmluZyxcclxuICBmaWxlczogQXJyYXk8RmlsZUhhbmRsZT4sXHJcbik6IFByb21pc2U8RG9jdW1lbnRDb250ZXh0SW5qZWN0aW9uU3RyYXRlZ3k+IHtcclxuICBjb25zdCBzdGF0dXMgPSBjdGwuY3JlYXRlU3RhdHVzKHtcclxuICAgIHN0YXR1czogXCJsb2FkaW5nXCIsXHJcbiAgICB0ZXh0OiBgRGVjaWRpbmcgaG93IHRvIGhhbmRsZSB0aGUgZG9jdW1lbnQocykuLi5gLFxyXG4gIH0pO1xyXG5cclxuICBjb25zdCBtb2RlbCA9IGF3YWl0IGN0bC5jbGllbnQubGxtLm1vZGVsKCk7XHJcbiAgY29uc3QgY3R4ID0gYXdhaXQgY3RsLnB1bGxIaXN0b3J5KCk7XHJcblxyXG4gIC8vIE1lYXN1cmUgdGhlIGNvbnRleHQgd2luZG93XHJcbiAgY29uc3Qge1xyXG4gICAgdG90YWxUb2tlbnNJbkNvbnRleHQsXHJcbiAgICBtb2RlbENvbnRleHRMZW5ndGgsXHJcbiAgICBtb2RlbFJlbWFpbmluZ0NvbnRleHRMZW5ndGgsXHJcbiAgICBjb250ZXh0T2NjdXBpZWRQZXJjZW50LFxyXG4gIH0gPSBhd2FpdCBtZWFzdXJlQ29udGV4dFdpbmRvdyhjdHgsIG1vZGVsKTtcclxuXHJcbiAgY3RsLmRlYnVnKFxyXG4gICAgYENvbnRleHQgbWVhc3VyZW1lbnQgcmVzdWx0OlxcblxcbmAgK1xyXG4gICAgICBgXFx0VG90YWwgdG9rZW5zIGluIGNvbnRleHQ6ICR7dG90YWxUb2tlbnNJbkNvbnRleHR9XFxuYCArXHJcbiAgICAgIGBcXHRNb2RlbCBjb250ZXh0IGxlbmd0aDogJHttb2RlbENvbnRleHRMZW5ndGh9XFxuYCArXHJcbiAgICAgIGBcXHRNb2RlbCByZW1haW5pbmcgY29udGV4dCBsZW5ndGg6ICR7bW9kZWxSZW1haW5pbmdDb250ZXh0TGVuZ3RofVxcbmAgK1xyXG4gICAgICBgXFx0Q29udGV4dCBvY2N1cGllZCBwZXJjZW50OiAke2NvbnRleHRPY2N1cGllZFBlcmNlbnQudG9GaXhlZCgyKX0lXFxuYCxcclxuICApO1xyXG5cclxuICAvLyBHZXQgdG9rZW4gY291bnQgb2YgcHJvdmlkZWQgZmlsZXNcclxuICBsZXQgdG90YWxGaWxlVG9rZW5Db3VudCA9IDA7XHJcbiAgbGV0IHRvdGFsUmVhZFRpbWUgPSAwO1xyXG4gIGxldCB0b3RhbFRva2VuaXplVGltZSA9IDA7XHJcbiAgZm9yIChjb25zdCBmaWxlIG9mIGZpbGVzKSB7XHJcbiAgICBjb25zdCBzdGFydFRpbWUgPSBwZXJmb3JtYW5jZS5ub3coKTtcclxuXHJcbiAgICBjb25zdCBsb2FkaW5nU3RhdHVzID0gc3RhdHVzLmFkZFN1YlN0YXR1cyh7XHJcbiAgICAgIHN0YXR1czogXCJsb2FkaW5nXCIsXHJcbiAgICAgIHRleHQ6IGBMb2FkaW5nIHBhcnNlciBmb3IgJHtmaWxlLm5hbWV9Li4uYCxcclxuICAgIH0pO1xyXG4gICAgbGV0IGFjdGlvblByb2dyZXNzaW5nID0gXCJSZWFkaW5nXCI7XHJcbiAgICBsZXQgcGFyc2VySW5kaWNhdG9yID0gXCJcIjtcclxuXHJcbiAgICBjb25zdCB7IGNvbnRlbnQgfSA9IGF3YWl0IGN0bC5jbGllbnQuZmlsZXMucGFyc2VEb2N1bWVudChmaWxlLCB7XHJcbiAgICAgIHNpZ25hbDogY3RsLmFib3J0U2lnbmFsLFxyXG4gICAgICBvblBhcnNlckxvYWRlZDogcGFyc2VyID0+IHtcclxuICAgICAgICBsb2FkaW5nU3RhdHVzLnNldFN0YXRlKHtcclxuICAgICAgICAgIHN0YXR1czogXCJsb2FkaW5nXCIsXHJcbiAgICAgICAgICB0ZXh0OiBgJHtwYXJzZXIubGlicmFyeX0gbG9hZGVkIGZvciAke2ZpbGUubmFtZX0uLi5gLFxyXG4gICAgICAgIH0pO1xyXG4gICAgICAgIC8vIFVwZGF0ZSBhY3Rpb24gbmFtZXMgaWYgd2UncmUgdXNpbmcgYSBwYXJzaW5nIGZyYW1ld29ya1xyXG4gICAgICAgIGlmIChwYXJzZXIubGlicmFyeSAhPT0gXCJidWlsdEluXCIpIHtcclxuICAgICAgICAgIGFjdGlvblByb2dyZXNzaW5nID0gXCJQYXJzaW5nXCI7XHJcbiAgICAgICAgICBwYXJzZXJJbmRpY2F0b3IgPSBgIHdpdGggJHtwYXJzZXIubGlicmFyeX1gO1xyXG4gICAgICAgIH1cclxuICAgICAgfSxcclxuICAgICAgb25Qcm9ncmVzczogcHJvZ3Jlc3MgPT4ge1xyXG4gICAgICAgIGxvYWRpbmdTdGF0dXMuc2V0U3RhdGUoe1xyXG4gICAgICAgICAgc3RhdHVzOiBcImxvYWRpbmdcIixcclxuICAgICAgICAgIHRleHQ6IGAke2FjdGlvblByb2dyZXNzaW5nfSBmaWxlICR7ZmlsZS5uYW1lfSR7cGFyc2VySW5kaWNhdG9yfS4uLiAoJHsoXHJcbiAgICAgICAgICAgIHByb2dyZXNzICogMTAwXHJcbiAgICAgICAgICApLnRvRml4ZWQoMil9JSlgLFxyXG4gICAgICAgIH0pO1xyXG4gICAgICB9LFxyXG4gICAgfSk7XHJcbiAgICBsb2FkaW5nU3RhdHVzLnJlbW92ZSgpO1xyXG5cclxuICAgIHRvdGFsUmVhZFRpbWUgKz0gcGVyZm9ybWFuY2Uubm93KCkgLSBzdGFydFRpbWU7XHJcblxyXG4gICAgLy8gdG9rZW5pemUgZmlsZSBjb250ZW50XHJcbiAgICBjb25zdCBzdGFydFRva2VuaXplVGltZSA9IHBlcmZvcm1hbmNlLm5vdygpO1xyXG4gICAgdG90YWxGaWxlVG9rZW5Db3VudCArPSBhd2FpdCBtb2RlbC5jb3VudFRva2Vucyhjb250ZW50KTtcclxuICAgIHRvdGFsVG9rZW5pemVUaW1lICs9IHBlcmZvcm1hbmNlLm5vdygpIC0gc3RhcnRUb2tlbml6ZVRpbWU7XHJcbiAgICBpZiAodG90YWxGaWxlVG9rZW5Db3VudCA+IG1vZGVsUmVtYWluaW5nQ29udGV4dExlbmd0aCkge1xyXG4gICAgICAvLyBFYXJseSBleGl0IGlmIHdlIGFscmVhZHkgaGF2ZSB0b28gbXVjaCB0b2tlbnMuIEhlbHBzIHdpdGggcGVyZm9ybWFuY2Ugd2hlbiB0aGVyZSBhcmUgYSBsb3Qgb2YgZmlsZXMuXHJcbiAgICAgIGJyZWFrO1xyXG4gICAgfVxyXG4gIH1cclxuICBjdGwuZGVidWcoYFRvdGFsIGZpbGUgcmVhZCB0aW1lOiAke3RvdGFsUmVhZFRpbWUudG9GaXhlZCgyKX0gbXNgKTtcclxuICBjdGwuZGVidWcoYFRvdGFsIHRva2VuaXplIHRpbWU6ICR7dG90YWxUb2tlbml6ZVRpbWUudG9GaXhlZCgyKX0gbXNgKTtcclxuXHJcbiAgLy8gQ2FsY3VsYXRlIHRvdGFsIHRva2VuIGNvdW50IG9mIGZpbGVzICsgdXNlciBwcm9tcHRcclxuICBjdGwuZGVidWcoYE9yaWdpbmFsIFVzZXIgUHJvbXB0OiAke29yaWdpbmFsVXNlclByb21wdH1gKTtcclxuICBjb25zdCB1c2VyUHJvbXB0VG9rZW5Db3VudCA9IChhd2FpdCBtb2RlbC50b2tlbml6ZShvcmlnaW5hbFVzZXJQcm9tcHQpKS5sZW5ndGg7XHJcbiAgY29uc3QgdG90YWxGaWxlUGx1c1Byb21wdFRva2VuQ291bnQgPSB0b3RhbEZpbGVUb2tlbkNvdW50ICsgdXNlclByb21wdFRva2VuQ291bnQ7XHJcblxyXG4gIC8vIENhbGN1bGF0ZSB0aGUgYXZhaWxhYmxlIGNvbnRleHQgdG9rZW5zXHJcbiAgY29uc3QgY29udGV4dE9jY3VwaWVkRnJhY3Rpb24gPSBjb250ZXh0T2NjdXBpZWRQZXJjZW50IC8gMTAwO1xyXG4gIGNvbnN0IHRhcmdldENvbnRleHRVc2VQZXJjZW50ID0gMC43O1xyXG4gIGNvbnN0IHRhcmdldENvbnRleHRVc2FnZSA9IHRhcmdldENvbnRleHRVc2VQZXJjZW50ICogKDEgLSBjb250ZXh0T2NjdXBpZWRGcmFjdGlvbik7XHJcbiAgY29uc3QgYXZhaWxhYmxlQ29udGV4dFRva2VucyA9IE1hdGguZmxvb3IobW9kZWxSZW1haW5pbmdDb250ZXh0TGVuZ3RoICogdGFyZ2V0Q29udGV4dFVzYWdlKTtcclxuXHJcbiAgLy8gRGVidWcgbG9nXHJcbiAgY3RsLmRlYnVnKFwiU3RyYXRlZ3kgQ2FsY3VsYXRpb246XCIpO1xyXG4gIGN0bC5kZWJ1ZyhgXFx0VG90YWwgVG9rZW5zIGluIEFsbCBGaWxlczogJHt0b3RhbEZpbGVUb2tlbkNvdW50fWApO1xyXG4gIGN0bC5kZWJ1ZyhgXFx0VG90YWwgVG9rZW5zIGluIFVzZXIgUHJvbXB0OiAke3VzZXJQcm9tcHRUb2tlbkNvdW50fWApO1xyXG4gIGN0bC5kZWJ1ZyhgXFx0TW9kZWwgQ29udGV4dCBSZW1haW5pbmc6ICR7bW9kZWxSZW1haW5pbmdDb250ZXh0TGVuZ3RofSB0b2tlbnNgKTtcclxuICBjdGwuZGVidWcoYFxcdENvbnRleHQgT2NjdXBpZWQ6ICR7Y29udGV4dE9jY3VwaWVkUGVyY2VudC50b0ZpeGVkKDIpfSVgKTtcclxuICBjdGwuZGVidWcoYFxcdEF2YWlsYWJsZSBUb2tlbnM6ICR7YXZhaWxhYmxlQ29udGV4dFRva2Vuc31cXG5gKTtcclxuXHJcbiAgaWYgKHRvdGFsRmlsZVBsdXNQcm9tcHRUb2tlbkNvdW50ID4gYXZhaWxhYmxlQ29udGV4dFRva2Vucykge1xyXG4gICAgY29uc3QgY2hvc2VuU3RyYXRlZ3kgPSBcInJldHJpZXZhbFwiO1xyXG4gICAgY3RsLmRlYnVnKFxyXG4gICAgICBgQ2hvc2VuIGNvbnRleHQgaW5qZWN0aW9uIHN0cmF0ZWd5OiAnJHtjaG9zZW5TdHJhdGVneX0nLiBUb3RhbCBmaWxlICsgcHJvbXB0IHRva2VuIGNvdW50OiBgICtcclxuICAgICAgICBgJHt0b3RhbEZpbGVQbHVzUHJvbXB0VG9rZW5Db3VudH0gPiAke1xyXG4gICAgICAgICAgdGFyZ2V0Q29udGV4dFVzYWdlICogMTAwXHJcbiAgICAgICAgfSUgKiBhdmFpbGFibGUgY29udGV4dCB0b2tlbnM6ICR7YXZhaWxhYmxlQ29udGV4dFRva2Vuc31gLFxyXG4gICAgKTtcclxuICAgIHN0YXR1cy5zZXRTdGF0ZSh7XHJcbiAgICAgIHN0YXR1czogXCJkb25lXCIsXHJcbiAgICAgIHRleHQ6IGBDaG9zZW4gY29udGV4dCBpbmplY3Rpb24gc3RyYXRlZ3k6ICcke2Nob3NlblN0cmF0ZWd5fScuIFJldHJpZXZhbCBpcyBvcHRpbWFsIGZvciB0aGUgc2l6ZSBvZiBjb250ZW50IHByb3ZpZGVkYCxcclxuICAgIH0pO1xyXG4gICAgcmV0dXJuIGNob3NlblN0cmF0ZWd5O1xyXG4gIH1cclxuXHJcbiAgLy8gVE9ETzpcclxuICAvL1xyXG4gIC8vICAgQ29uc2lkZXIgYSBtb3JlIHNvcGhpc3RpY2F0ZWQgc3RyYXRlZ3kgd2hlcmUgd2UgaW5qZWN0IHNvbWUgaGVhZGVyIG9yIHN1bW1hcnkgY29udGVudFxyXG4gIC8vICAgYW5kIHRoZW4gcGVyZm9ybSByZXRyaWV2YWwgb24gdGhlIHJlc3Qgb2YgdGhlIGNvbnRlbnQuXHJcbiAgLy9cclxuICAvL1xyXG5cclxuICBjb25zdCBjaG9zZW5TdHJhdGVneSA9IFwiaW5qZWN0LWZ1bGwtY29udGVudFwiO1xyXG4gIHN0YXR1cy5zZXRTdGF0ZSh7XHJcbiAgICBzdGF0dXM6IFwiZG9uZVwiLFxyXG4gICAgdGV4dDogYENob3NlbiBjb250ZXh0IGluamVjdGlvbiBzdHJhdGVneTogJyR7Y2hvc2VuU3RyYXRlZ3l9Jy4gQWxsIGNvbnRlbnQgY2FuIGZpdCBpbnRvIHRoZSBjb250ZXh0YCxcclxuICB9KTtcclxuICByZXR1cm4gY2hvc2VuU3RyYXRlZ3k7XHJcbn1cclxuIiwgImltcG9ydCB7IHR5cGUgUGx1Z2luQ29udGV4dCB9IGZyb20gXCJAbG1zdHVkaW8vc2RrXCI7XHJcbmltcG9ydCB7IGNvbmZpZ1NjaGVtYXRpY3MgfSBmcm9tIFwiLi9jb25maWdcIjtcclxuaW1wb3J0IHsgcHJlcHJvY2VzcyB9IGZyb20gXCIuL3Byb21wdFByZXByb2Nlc3NvclwiO1xyXG5cclxuLy8gVGhpcyBpcyB0aGUgZW50cnkgcG9pbnQgb2YgdGhlIHBsdWdpbi4gVGhlIG1haW4gZnVuY3Rpb24gaXMgdG8gcmVnaXN0ZXIgZGlmZmVyZW50IGNvbXBvbmVudHMgb2ZcclxuLy8gdGhlIHBsdWdpbiwgc3VjaCBhcyBwcm9tcHRQcmVwcm9jZXNzb3IsIHByZWRpY3Rpb25Mb29wSGFuZGxlciwgZXRjLlxyXG4vL1xyXG4vLyBZb3UgZG8gbm90IG5lZWQgdG8gbW9kaWZ5IHRoaXMgZmlsZSB1bmxlc3MgeW91IHdhbnQgdG8gYWRkIG1vcmUgY29tcG9uZW50cyB0byB0aGUgcGx1Z2luLCBhbmQvb3JcclxuLy8gYWRkIGN1c3RvbSBpbml0aWFsaXphdGlvbiBsb2dpYy5cclxuXHJcbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBtYWluKGNvbnRleHQ6IFBsdWdpbkNvbnRleHQpIHtcclxuICAvLyBSZWdpc3RlciB0aGUgY29uZmlndXJhdGlvbiBzY2hlbWF0aWNzLlxyXG4gIGNvbnRleHQud2l0aENvbmZpZ1NjaGVtYXRpY3MoY29uZmlnU2NoZW1hdGljcyk7XHJcbiAgLy8gUmVnaXN0ZXIgdGhlIHByb21wdFByZXByb2Nlc3Nvci5cclxuICBjb250ZXh0LndpdGhQcm9tcHRQcmVwcm9jZXNzb3IocHJlcHJvY2Vzcyk7XHJcbn1cclxuIiwgImltcG9ydCB7IExNU3R1ZGlvQ2xpZW50LCB0eXBlIFBsdWdpbkNvbnRleHQgfSBmcm9tIFwiQGxtc3R1ZGlvL3Nka1wiO1xuXG5kZWNsYXJlIHZhciBwcm9jZXNzOiBhbnk7XG5cbi8vIFdlIHJlY2VpdmUgcnVudGltZSBpbmZvcm1hdGlvbiBpbiB0aGUgZW52aXJvbm1lbnQgdmFyaWFibGVzLlxuY29uc3QgY2xpZW50SWRlbnRpZmllciA9IHByb2Nlc3MuZW52LkxNU19QTFVHSU5fQ0xJRU5UX0lERU5USUZJRVI7XG5jb25zdCBjbGllbnRQYXNza2V5ID0gcHJvY2Vzcy5lbnYuTE1TX1BMVUdJTl9DTElFTlRfUEFTU0tFWTtcbmNvbnN0IGJhc2VVcmwgPSBwcm9jZXNzLmVudi5MTVNfUExVR0lOX0JBU0VfVVJMO1xuXG5jb25zdCBjbGllbnQgPSBuZXcgTE1TdHVkaW9DbGllbnQoe1xuICBjbGllbnRJZGVudGlmaWVyLFxuICBjbGllbnRQYXNza2V5LFxuICBiYXNlVXJsLFxufSk7XG5cbihnbG9iYWxUaGlzIGFzIGFueSkuX19MTVNfUExVR0lOX0NPTlRFWFQgPSB0cnVlO1xuXG5sZXQgcHJlZGljdGlvbkxvb3BIYW5kbGVyU2V0ID0gZmFsc2U7XG5sZXQgcHJvbXB0UHJlcHJvY2Vzc29yU2V0ID0gZmFsc2U7XG5sZXQgY29uZmlnU2NoZW1hdGljc1NldCA9IGZhbHNlO1xubGV0IGdsb2JhbENvbmZpZ1NjaGVtYXRpY3NTZXQgPSBmYWxzZTtcbmxldCB0b29sc1Byb3ZpZGVyU2V0ID0gZmFsc2U7XG5sZXQgZ2VuZXJhdG9yU2V0ID0gZmFsc2U7XG5cbmNvbnN0IHNlbGZSZWdpc3RyYXRpb25Ib3N0ID0gY2xpZW50LnBsdWdpbnMuZ2V0U2VsZlJlZ2lzdHJhdGlvbkhvc3QoKTtcblxuY29uc3QgcGx1Z2luQ29udGV4dDogUGx1Z2luQ29udGV4dCA9IHtcbiAgd2l0aFByZWRpY3Rpb25Mb29wSGFuZGxlcjogKGdlbmVyYXRlKSA9PiB7XG4gICAgaWYgKHByZWRpY3Rpb25Mb29wSGFuZGxlclNldCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFwiUHJlZGljdGlvbkxvb3BIYW5kbGVyIGFscmVhZHkgcmVnaXN0ZXJlZFwiKTtcbiAgICB9XG4gICAgaWYgKHRvb2xzUHJvdmlkZXJTZXQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihcIlByZWRpY3Rpb25Mb29wSGFuZGxlciBjYW5ub3QgYmUgdXNlZCB3aXRoIGEgdG9vbHMgcHJvdmlkZXJcIik7XG4gICAgfVxuXG4gICAgcHJlZGljdGlvbkxvb3BIYW5kbGVyU2V0ID0gdHJ1ZTtcbiAgICBzZWxmUmVnaXN0cmF0aW9uSG9zdC5zZXRQcmVkaWN0aW9uTG9vcEhhbmRsZXIoZ2VuZXJhdGUpO1xuICAgIHJldHVybiBwbHVnaW5Db250ZXh0O1xuICB9LFxuICB3aXRoUHJvbXB0UHJlcHJvY2Vzc29yOiAocHJlcHJvY2VzcykgPT4ge1xuICAgIGlmIChwcm9tcHRQcmVwcm9jZXNzb3JTZXQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihcIlByb21wdFByZXByb2Nlc3NvciBhbHJlYWR5IHJlZ2lzdGVyZWRcIik7XG4gICAgfVxuICAgIHByb21wdFByZXByb2Nlc3NvclNldCA9IHRydWU7XG4gICAgc2VsZlJlZ2lzdHJhdGlvbkhvc3Quc2V0UHJvbXB0UHJlcHJvY2Vzc29yKHByZXByb2Nlc3MpO1xuICAgIHJldHVybiBwbHVnaW5Db250ZXh0O1xuICB9LFxuICB3aXRoQ29uZmlnU2NoZW1hdGljczogKGNvbmZpZ1NjaGVtYXRpY3MpID0+IHtcbiAgICBpZiAoY29uZmlnU2NoZW1hdGljc1NldCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFwiQ29uZmlnIHNjaGVtYXRpY3MgYWxyZWFkeSByZWdpc3RlcmVkXCIpO1xuICAgIH1cbiAgICBjb25maWdTY2hlbWF0aWNzU2V0ID0gdHJ1ZTtcbiAgICBzZWxmUmVnaXN0cmF0aW9uSG9zdC5zZXRDb25maWdTY2hlbWF0aWNzKGNvbmZpZ1NjaGVtYXRpY3MpO1xuICAgIHJldHVybiBwbHVnaW5Db250ZXh0O1xuICB9LFxuICB3aXRoR2xvYmFsQ29uZmlnU2NoZW1hdGljczogKGdsb2JhbENvbmZpZ1NjaGVtYXRpY3MpID0+IHtcbiAgICBpZiAoZ2xvYmFsQ29uZmlnU2NoZW1hdGljc1NldCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFwiR2xvYmFsIGNvbmZpZyBzY2hlbWF0aWNzIGFscmVhZHkgcmVnaXN0ZXJlZFwiKTtcbiAgICB9XG4gICAgZ2xvYmFsQ29uZmlnU2NoZW1hdGljc1NldCA9IHRydWU7XG4gICAgc2VsZlJlZ2lzdHJhdGlvbkhvc3Quc2V0R2xvYmFsQ29uZmlnU2NoZW1hdGljcyhnbG9iYWxDb25maWdTY2hlbWF0aWNzKTtcbiAgICByZXR1cm4gcGx1Z2luQ29udGV4dDtcbiAgfSxcbiAgd2l0aFRvb2xzUHJvdmlkZXI6ICh0b29sc1Byb3ZpZGVyKSA9PiB7XG4gICAgaWYgKHRvb2xzUHJvdmlkZXJTZXQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihcIlRvb2xzIHByb3ZpZGVyIGFscmVhZHkgcmVnaXN0ZXJlZFwiKTtcbiAgICB9XG4gICAgaWYgKHByZWRpY3Rpb25Mb29wSGFuZGxlclNldCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFwiVG9vbHMgcHJvdmlkZXIgY2Fubm90IGJlIHVzZWQgd2l0aCBhIHByZWRpY3Rpb25Mb29wSGFuZGxlclwiKTtcbiAgICB9XG5cbiAgICB0b29sc1Byb3ZpZGVyU2V0ID0gdHJ1ZTtcbiAgICBzZWxmUmVnaXN0cmF0aW9uSG9zdC5zZXRUb29sc1Byb3ZpZGVyKHRvb2xzUHJvdmlkZXIpO1xuICAgIHJldHVybiBwbHVnaW5Db250ZXh0O1xuICB9LFxuICB3aXRoR2VuZXJhdG9yOiAoZ2VuZXJhdG9yKSA9PiB7XG4gICAgaWYgKGdlbmVyYXRvclNldCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKFwiR2VuZXJhdG9yIGFscmVhZHkgcmVnaXN0ZXJlZFwiKTtcbiAgICB9XG5cbiAgICBnZW5lcmF0b3JTZXQgPSB0cnVlO1xuICAgIHNlbGZSZWdpc3RyYXRpb25Ib3N0LnNldEdlbmVyYXRvcihnZW5lcmF0b3IpO1xuICAgIHJldHVybiBwbHVnaW5Db250ZXh0O1xuICB9LFxufTtcblxuaW1wb3J0KFwiLi8uLi9zcmMvaW5kZXgudHNcIikudGhlbihhc3luYyBtb2R1bGUgPT4ge1xuICByZXR1cm4gYXdhaXQgbW9kdWxlLm1haW4ocGx1Z2luQ29udGV4dCk7XG59KS50aGVuKCgpID0+IHtcbiAgc2VsZlJlZ2lzdHJhdGlvbkhvc3QuaW5pdENvbXBsZXRlZCgpO1xufSkuY2F0Y2goKGVycm9yKSA9PiB7XG4gIGNvbnNvbGUuZXJyb3IoXCJGYWlsZWQgdG8gZXhlY3V0ZSB0aGUgbWFpbiBmdW5jdGlvbiBvZiB0aGUgcGx1Z2luLlwiKTtcbiAgY29uc29sZS5lcnJvcihlcnJvcik7XG59KTtcbiJdLAogICJtYXBwaW5ncyI6ICI7Ozs7Ozs7Ozs7OztBQUFBLGdCQUVhO0FBRmI7QUFBQTtBQUFBO0FBQUEsaUJBQXVDO0FBRWhDLElBQU0sdUJBQW1CLG1DQUF1QixFQUNwRDtBQUFBLE1BQ0M7QUFBQSxNQUNBO0FBQUEsTUFDQTtBQUFBLFFBQ0UsS0FBSztBQUFBLFFB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QUFDNUIsWUFBTSxJQUFJLE1BQU0sMENBQTBDO0FBQUEsSUFDNUQ7QUFDQSxRQUFJLGtCQUFrQjtBQUNwQixZQUFNLElBQUksTUFBTSw0REFBNEQ7QUFBQSxJQUM5RTtBQUVBLCtCQUEyQjtBQUMzQix5QkFBcUIseUJBQXlCLFFBQVE7QUFDdEQsV0FBTztBQUFBLEVBQ1Q7QUFBQSxFQUNBLHdCQUF3QixDQUFDQyxnQkFBZTtBQUN0QyxRQUFJLHVCQUF1QjtBQUN6QixZQUFNLElBQUksTUFBTSx1Q0FBdUM7QUFBQSxJQUN6RDtBQUNBLDRCQUF3QjtBQUN4Qix5QkFBcUIsc0JBQXNCQSxXQUFVO0FBQ3JELFdBQU87QUFBQSxFQUNUO0FBQUEsRUFDQSxzQkFBc0IsQ0FBQ0Msc0JBQXFCO0FBQzFDLFFBQUkscUJBQXFCO0FBQ3ZCLFlBQU0sSUFBSSxNQUFNLHNDQUFzQztBQUFBLElBQ3hEO0FBQ0EsMEJBQXNCO0FBQ3RCLHlCQUFxQixvQkFBb0JBLGlCQUFnQjtBQUN6RCxXQUFPO0FBQUEsRUFDVDtBQUFBLEVBQ0EsNEJBQTRCLENBQUMsMkJBQTJCO0FBQ3RELFFBQUksMkJBQTJCO0FBQzdCLFlBQU0sSUFBSSxNQUFNLDZDQUE2QztBQUFBLElBQy9EO0FBQ0EsZ0NBQTRCO0FBQzVCLHlCQUFxQiwwQkFBMEIsc0JBQXNCO0FBQ3JFLFdBQU87QUFBQSxFQUNUO0FBQUEsRUFDQSxtQkFBbUIsQ0FBQyxrQkFBa0I7QUFDcEMsUUFBSSxrQkFBa0I7QUFDcEIsWUFBTSxJQUFJLE1BQU0sbUNBQW1DO0FBQUEsSUFDckQ7QUFDQSxRQUFJLDBCQUEwQjtBQUM1QixZQUFNLElBQUksTUFBTSw0REFBNEQ7QUFBQSxJQUM5RTtBQUVBLHVCQUFtQjtBQUNuQix5QkFBcUIsaUJBQWlCLGFBQWE7QUFDbkQsV0FBTztBQUFBLEVBQ1Q7QUFBQSxFQUNBLGVBQWUsQ0FBQyxjQUFjO0FBQzVCLFFBQUksY0FBYztBQUNoQixZQUFNLElBQUksTUFBTSw4QkFBOEI7QUFBQSxJQUNoRDtBQUVBLG1CQUFlO0FBQ2YseUJBQXFCLGFBQWEsU0FBUztBQUMzQyxXQUFPO0FBQUEsRUFDVDtBQUNGO0FBRUEsd0RBQTRCLEtBQUssT0FBTUMsWUFBVTtBQUMvQyxTQUFPLE1BQU1BLFFBQU8sS0FBSyxhQUFhO0FBQ3hDLENBQUMsRUFBRSxLQUFLLE1BQU07QUFDWix1QkFBcUIsY0FBYztBQUNyQyxDQUFDLEVBQUUsTUFBTSxDQUFDLFVBQVU7QUFDbEIsVUFBUSxNQUFNLG9EQUFvRDtBQUNsRSxVQUFRLE1BQU0sS0FBSztBQUNyQixDQUFDOyIsCiAgIm5hbWVzIjogWyJyZXN1bHQiLCAiY2hvc2VuU3RyYXRlZ3kiLCAiaW1wb3J0X3NkayIsICJpbXBvcnRfc2RrIiwgInByZXByb2Nlc3MiLCAiY29uZmlnU2NoZW1hdGljcyIsICJtb2R1bGUiXQp9Cg==
