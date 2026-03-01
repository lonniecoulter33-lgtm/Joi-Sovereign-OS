import { getFromQueryParams } from "./utils.js";

export const networkCall = async (endpoint, params = {}, options = {}) => {
  let finalUrl = addParametersToUrl(getBaseAPIUrl() + endpoint, params);
  let res = await fetch(finalUrl, options);
  res = res.json();
  console.log(res);
  return res;
};

const getBaseAPIUrl = () => {
  let env = getFromQueryParams("env");
  if (!env) {
    if (window.location.href.includes("prod")) {
      env = "prod";
    } else {
      env = "engg";
    }
  }
  if (env == "prod") {
    return "https://wallet.now.gg/notify/v1";
  } else {
    return "https://crypto-wallet-engg1.stagingngg.net/notify/v1";
  }
};
export const getCDNHostUrl = () => {
  let env = getFromQueryParams("env");
  if (!env) {
    if (window.location.href.includes("prod")) {
      env = "prod";
    } else {
      env = "engg";
    }
  }
  if (env == "prod") {
    return "https://wallet-cdn.now.gg";
  } else {
    return "https://crypto-blockchain-cdn.now.gg";
  }
};

const addParametersToUrl = (url, parameters) => {
  if (!parameters) return url;
  let paramUrl = url;
  if (parameters) {
    if (paramUrl.includes("?")) {
      paramUrl += "&";
    } else {
      paramUrl += "?";
    }
    for (var param in parameters) {
      paramUrl += param + "=" + parameters[param] + "&";
    }
    paramUrl = paramUrl.substring(0, paramUrl.length - 1);
  }
  return paramUrl;
};
