import { translationResources, fallbackLng } from "../i18n/resources.js";
import { getFromQueryParams } from "../js/utils.js";

let preferredLanguage = getFromQueryParams('lang');
i18next.init({
  fallbackLng: fallbackLng,
  lng: preferredLanguage,
  resources: translationResources,
});
