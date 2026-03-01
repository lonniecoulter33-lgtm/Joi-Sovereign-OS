import { getCDNHostUrl, networkCall } from "./network.js";
import { APIEndpoints } from "./constants.js";
import { getFromQueryParams } from "./utils.js";

window.sendMessageToElectronApp = function (payload) {
  console.log("Sending message to electron ======> " + payload.action)
  if (window.electron) {
    let { send } = window.electron;
    send(payload);
  }
};

var lang = getFromQueryParams("lang")
var authToken = getFromQueryParams("auth_token")

var categories = [
];
var toggleState = {};
var machineDetails = {};


if (window.electron) {
  let { onMessage: _onMessage } = window.electron
  _onMessage(async (payload) => {
    console.log('Inside Electron onMessage listener')
    console.log(payload)
    let { wallet_guid, bs5_guid, bsx_guid, wallet_version, bs5_version, bsx_version, action, response } = payload || {}
    if (wallet_guid) {
      machineDetails["wallet_guid"] = wallet_guid
    }
    if (bsx_guid) {
      machineDetails["bsx_guid"] = bsx_guid
    }
    if (bs5_guid) {
      machineDetails["bs5_guid"] = bs5_guid
    }
    if (wallet_version) {
      machineDetails["wallet_version"] = wallet_version
    }
    if (bsx_version) {
      machineDetails["bsx_version"] = bsx_version
    }
    if (bs5_version) {
      machineDetails["bs5_version"] = bs5_version
    }
    if (action == "GET_NOTIF_PREFERENCES") {
      categories.map((category) => {
        if (response && response[category.id]) {
          document.getElementById(category.id).checked = response[category.id]?.value;
          toggleState[category.id] = response[category.id]?.value;
        }
        else {
          window.sendMessageToElectronApp({
            action: "SET_NOTIF_PREFERENCES", actionParams: {
              category_id: category.id,
              value: category.default
            }
          })
        }
      })
      document.getElementById("loader").style.display = 'none';
      document.getElementById("categories").style.display = 'flex';
    }
    else if (action == "SET_NOTIF_PREFERENCES") {
      let { wallet_guid, bs5_guid, bsx_guid, wallet_version, bs5_version, bsx_version } = machineDetails || {}
      let { success, category_id } = response || {}
      if (category_id) {
        if (!success) {
          try {
            await networkCall(APIEndpoints.toggleNotificationCategory, null, {
              method: "PUT",
              body: JSON.stringify({
                notification_category: category_id,
                enabled: document.getElementById(category_id).checked,
                source: 'bs_services',
                bsx_guid: bsx_guid,
                bs5_guid: bs5_guid,
                wallet_guid: wallet_guid,
                lang: lang,
                bsx_version: bsx_version,
                bs5_version: bs5_version,
                wallet_version: wallet_version,
              }),
              headers: { "Content-Type": "application/json", "Authorization": authToken ?? "testing" },
            });
            document.getElementById(category_id).checked = toggleState[category_id];
            showErrorSnackbar()
          }
          catch (e) {
            console.log(e);
          }
        }
        else {
          if (toggleState[category_id] != null && toggleState[category_id] != undefined) {
            toggleState[category_id] = !toggleState[category_id];
          }
          else {
            toggleState[category_id] = categories.filter((c) => c.id == category_id)[0].default
          }
        }
        document.getElementById(category_id).disabled = false;
      }
    }
  })
}

async function fetchNotificationCategories() {
  await fetch(`${getCDNHostUrl()}/notify/v1/notification-categories?lang=${lang}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch file");
      }
      return response.text();
    })
    .then((result) => {
      var decodedResult = JSON.parse(result);
      categories = decodedResult?.data?.categories;
      window.sendMessageToElectronApp({ action: "GET_NOTIF_PREFERENCES" });
      let str = "";
      categories.forEach(function (category) {
        str +=
          `<div class="category">
                <div class="category-name">${category.name}</div>
                <label class="switch">
                    <input type="checkbox" id="${category.id}" name="${category.id}" ${category.default ? 'checked' : ''} />
                    <span class="slider round"></span>
                </label>
            </div>`
      });
      window.sendMessageToElectronApp({
        action: "SET_WINDOW_SIZE", actionParams: {
          width: 500,
          height: 272 + categories.length * 19.5
        }
      });
      document.getElementById('home').style.display = 'flex'
      document.getElementById('tab1').style.margin = 'unset'
      document.getElementById('fetchError').style.display = 'none'
      document.getElementById("categories").style.display = 'none';
      document.getElementById("categories").innerHTML = str;
      categories.forEach(category => {
        document.getElementById(category.id).addEventListener('click', debounce(onCategoryValueChange(category), 1000));
      })
    })
    .catch((error) => {
      document.getElementById('home').style.display = 'none'
      document.getElementById('tab1').style.margin = 'auto'
      document.getElementById('fetchError').style.display = 'flex'
    });
}
fetchNotificationCategories()

function onCategoryValueChange(category) {
  return async (e) => {
    if (e.target.checked != toggleState[category.id]) {
      e.target.disabled = true;
      let { wallet_guid, bs5_guid, bsx_guid, wallet_version, bs5_version, bsx_version } = machineDetails || {};
      try {
        if (!window.navigator.onLine) {
          throw "You are not connected to the internet";
        }
        else {
          let response = await networkCall(APIEndpoints.toggleNotificationCategory, null, {
            method: "PUT",
            body: JSON.stringify({
              notification_category: category.id,
              enabled: e.target.checked,
              source: 'bs_services',
              bsx_guid: bsx_guid,
              bs5_guid: bs5_guid,
              wallet_guid: wallet_guid,
              lang: lang,
              bsx_version: bsx_version,
              bs5_version: bs5_version,
              wallet_version: wallet_version,
            }),
            headers: { "Content-Type": "application/json", "Authorization": authToken ?? "testing" },
          });
          if (response?.success) {
            window.sendMessageToElectronApp({
              action: "SET_NOTIF_PREFERENCES", actionParams: {
                category_id: category.id,
                value: e.target.checked ? 1 : 0
              }
            });
          }
          else {
            throw "Unable to toggle category";
          }
        }
      }
      catch (error) {
        e.target.checked = toggleState[category.id];
        e.target.disabled = false;
        showErrorSnackbar();
      }
    }
  };
}

function debounce(fn, wait, callFirst) {
  var timeout = null;
  var debouncedFn = null;

  var clear = function () {
    if (timeout) {
      clearTimeout(timeout);

      debouncedFn = null;
      timeout = null;
    }
  };

  var flush = function () {
    var call = debouncedFn;
    clear();

    if (call) {
      call();
    }
  };

  var debounceWrapper = function () {
    if (!wait) {
      return fn.apply(this, arguments);
    }

    var context = this;
    var args = arguments;
    var callNow = callFirst && !timeout;
    clear();

    debouncedFn = function () {
      fn.apply(context, args);
    };

    timeout = setTimeout(function () {
      timeout = null;

      if (!callNow) {
        var call = debouncedFn;
        debouncedFn = null;

        return call();
      }
    }, wait);

    if (callNow) {
      return debouncedFn();
    }
  };

  debounceWrapper.cancel = clear;
  debounceWrapper.flush = flush;

  return debounceWrapper;
}

function showErrorSnackbar() {
  var x = document.getElementById("snackbar")
  x.classList.add("show");
  setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
}

function closeApp() {
  window.sendMessageToElectronApp({ action: "CLOSE" });
}
document.getElementById('close-app').addEventListener('click', closeApp);

function openTermsOfUse() {
  window.sendMessageToElectronApp({ action: "OPEN_LINK", actionParams: { link: "https://www.bluestacks.com/terms-and-privacy.html" } });
}
document.getElementById('termsOfUse').addEventListener('click', openTermsOfUse);

