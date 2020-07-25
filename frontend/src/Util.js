import React, { useState, useEffect, useRef } from "react";
import { Redirect } from "react-router-dom";
import Cookies from "js-cookie";
import "./App.css";
const assert = require("assert");
let fetchInProgress = false;
let nextFetch = undefined;

const version = document.getElementById("backend-version").textContent.trim();

function CopyText(props) {
    const { text } = props;
    const ref = useRef(null);
    return (
        <>
            <span ref={ref}>{text}</span>{" "}
            <TLink
                className="CopyToClipboard"
                onClick={(event) => {
                    const range = document.createRange();
                    range.selectNodeContents(ref.current);
                    window.getSelection().removeAllRanges();
                    window.getSelection().addRange(range);
                    document.execCommand("copy");
                    window.getSelection().removeAllRanges();
                    event.target.blur();
                }}
            >
                (copy to clipboard)
            </TLink>
        </>
    );
}

function TLink(props) {
    const { className, onClick, children } = props;
    return (
        <button
            {...{ onClick }}
            type="button"
            className={"Link " + (className || "")}
        >
            {children}
        </button>
    );
}

function SLink(props) {
    const { className, onClick, children } = props;
    return (
        <button
            {...{ onClick }}
            type="button"
            className={"sLink material-icons " + (className || "")}
        >
            {children}
        </button>
    );
}

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
                    (err) => next.reject(err)
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
                    response_version
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
            headers: { "X-CSRFToken": Cookies.get("csrftoken") },
        },
        (response) => response
    );
}

function doPatch(url, data) {
    return doFetch(
        url,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify(data),
        },
        (response) => response.json()
    );
}

function doPost(url, data) {
    return doFetch(
        url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": Cookies.get("csrftoken"),
            },
            body: JSON.stringify(data),
        },
        (response) => response.json()
    );
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
                    setData((prev) => ({ ...prev, ...response }))
                )
                .catch((e) => {
                    if (e.name !== "AbortError") throw e;
                });
        },
    ];
}

function Save(props) {
    const { name, apiUrl, data, redirectUrl } = props;
    const [saving, setSaving] = useState("save");
    if (saving === "save")
        return (
            <TLink
                onClick={(event) => {
                    setSaving("saving");
                    doPost(apiUrl, data).then((response) =>
                        setSaving(response)
                    );
                }}
            >
                Save {name || ""}
            </TLink>
        );
    else if (saving === "saving") return <>Saving {name || ""}</>;
    else {
        const url =
            typeof redirectUrl === "function"
                ? redirectUrl(saving)
                : redirectUrl;
        return <Redirect to={url} />;
    }
}

function Delete(props) {
    const { name, apiUrl, redirectUrl } = props;
    const [state, setState] = useState("normal");
    if (state === "normal")
        return (
            <TLink
                onClick={(event) => {
                    setState("confirm");
                }}
            >
                Delete {name || ""}
            </TLink>
        );
    else if (state === "confirm")
        return (
            <TLink
                onClick={(event) => {
                    setState("deleting");
                    doDelete(apiUrl).then((response) => setState("deleted"));
                }}
            >
                Are you sure?
            </TLink>
        );
    else if (state === "deleting") return "Deleting";
    else if (state === "deleted") return <Redirect to={redirectUrl} />;
    else throw new Error(`unknown delete state: ${state}`);
}

function Overlay(props) {
    if (!props.message) return null;
    return (
        <div className="Overlay">
            <h1>{props.message}</h1>
        </div>
    );
}

function is(x: any, y: any) {
    return (
        (x === y && (x !== 0 || 1 / x === 1 / y)) || (x !== x && y !== y) // eslint-disable-line no-self-compare
    );
}
const hasOwnProperty = Object.prototype.hasOwnProperty;
function shallowEqual(objA: mixed, objB: mixed): boolean {
    if (is(objA, objB)) {
        return true;
    }

    if (
        typeof objA !== "object" ||
        objA === null ||
        typeof objB !== "object" ||
        objB === null
    ) {
        return false;
    }

    const keysA = Object.keys(objA);
    const keysB = Object.keys(objB);

    if (keysA.length !== keysB.length) {
        console.log("different keys", keysA, keysB);
        return false;
    }

    // Test for A's keys different from B.
    for (let i = 0; i < keysA.length; i++) {
        if (
            !hasOwnProperty.call(objB, keysA[i]) ||
            !is(objA[keysA[i]], objB[keysA[i]])
        ) {
            console.log(
                "different key",
                keysA[i],
                objA[keysA[i]],
                objB[keysA[i]]
            );
            return false;
        }
    }

    return true;
}

export {
    TLink,
    SLink,
    doPatch,
    doGet,
    doDelete,
    doPost,
    useData,
    version,
    Save,
    Delete,
    CopyText,
    fetchInProgress,
    Overlay,
    shallowEqual,
};
