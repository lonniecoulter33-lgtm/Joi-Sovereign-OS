import en from "./en.json" assert { type: "json" };
import fr from "./fr.json" assert { type: "json" };
import ar from "./ar.json" assert { type: "json" };
import de from "./de.json" assert { type: "json" };
import es from "./es.json" assert { type: "json" };
import id from "./id.json" assert { type: "json" };
import it from "./it.json" assert { type: "json" };
import ja from "./ja.json" assert { type: "json" };
import ko from "./ko.json" assert { type: "json" };
import pl from "./pl.json" assert { type: "json" };
import pt from "./pt.json" assert { type: "json" };
import ru from "./ru.json" assert { type: "json" };
import th from "./th.json" assert { type: "json" };
import tr from "./tr.json" assert { type: "json" };
import vi from "./vi.json" assert { type: "json" };
import zhCN from "./zh-CN.json" assert { type: "json" };
import zhTW from "./zh-TW.json" assert { type: "json" };

export const translationResources = {
  en: { translation: en },
  fr: { translation: fr },
  ar: { translation: ar },
  de: { translation: de },
  es: { translation: es },
  id: { translation: id },
  it: { translation: it },
  ja: { translation: ja },
  ko: { translation: ko },
  pl: { translation: pl },
  pt: { translation: pt },
  ru: { translation: ru },
  th: { translation: th },
  tr: { translation: tr },
  vi: { translation: vi },
  "zh-CN": { translation: zhCN },
  "zh-TW": { translation: zhTW },
};

export const fallbackLng = "en";
