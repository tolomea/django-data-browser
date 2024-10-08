import { useState, useEffect } from "react";

const assert = require("assert");
let fetchInProgress = false;
let nextFetch = undefined;

const version = document.getElementById("backend-version").textContent.trim();
const csrf_token = document.querySelector("[name=csrfmiddlewaretoken]").value;

class AbortError extends Error {
    name = "AbortError";
}

function doFetch(url, options, process) {
    if (fetchInProgress) {
        if (nextFetch) {
            nextFetch.reject(new AbortError("skipped"));
        }
        return new Promise((resolve, reject) => {
            nextFetch = { resolve, reject, url, options, process };
        });
    }

    fetchInProgress = true;

    return fetch(url, options)
        .then((response) => {
            // do we have a next fetch we need to trigger
            const next = nextFetch;
            nextFetch = undefined;
            fetchInProgress = false;

            if (next) {
                doFetch(next.url, next.options, next.process).then(
                    (res) => next.resolve(res),
                    (err) => next.reject(err),
                );
                throw new AbortError("superceeded");
            } else {
                return response;
            }
        })
        .then((response) => {
            // check status
            assert.ok(response.status >= 200);
            assert.ok(response.status < 300);
            return response;
        })
        .then((response) => {
            // check server version
            const response_version = response.headers.get("x-version");
            if (response_version !== version) {
                console.log(
                    "Version mismatch, hard reload",
                    version,
                    response_version,
                );
                window.location.reload(true);
            }
            return response;
        })
        .then((response) => process(response)); // process data
}

function doGet(url) {
    return doFetch(url, { method: "GET" }, (response) => response.json());
}

function doDelete(url) {
    return doFetch(
        url,
        {
            method: "DELETE",
            headers: { "X-CSRFToken": csrf_token },
        },
        (response) => response,
    );
}

function doPatch(url, data) {
    return doFetch(
        url,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify(data),
        },
        (response) => response.json(),
    );
}

function doPost(url, data) {
    return doFetch(
        url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token,
            },
            body: JSON.stringify(data),
        },
        (response) => response.json(),
    );
}

function syncPost(url, data) {
    const form = document.createElement("form");
    form.method = "post";
    form.action = url;

    data.push(["csrfmiddlewaretoken", csrf_token]);

    for (const [key, value] of data) {
        const hiddenField = document.createElement("input");
        hiddenField.type = "hidden";
        hiddenField.name = key;
        hiddenField.value = value;

        form.appendChild(hiddenField);
    }

    document.body.appendChild(form);
    form.submit();
}

function useData(url) {
    const [data, setData] = useState();
    useEffect(() => {
        doGet(url).then((response) => setData(response));
    }, [url]);
    return [
        data,
        (updates) => {
            setData((prev) => ({ ...prev, ...updates }));
            doPatch(url, updates)
                .then((response) =>
                    setData((prev) => ({ ...prev, ...response })),
                )
                .catch((e) => {
                    if (e.name !== "AbortError") throw e;
                });
        },
    ];
}

function useCData(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const abortController = new AbortController();

    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url, { signal: abortController.signal });
        const result = await response.json();
        if (isMounted) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (isMounted && err.name !== 'AbortError') {
          setError(err);
          setData(null);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
      abortController.abort();
    };
  }, [url]);

  return [data, loading, error];
}

export {
    doPatch,
    doGet,
    doDelete,
    doPost,
    useData,
    useCData,
    version,
    fetchInProgress,
    syncPost,
};
