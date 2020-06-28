import React, { useState, useEffect } from "react";
import { Redirect } from "react-router-dom";
import Cookies from "js-cookie";
import "./App.css";
let controller;
let fetchDescription;

const version = document.getElementById("backend-version").textContent.trim();

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

function doFetch(url, options, process) {
    if (controller) controller.abort();
    controller = new AbortController();
    fetchDescription = `${options.method} ${url}`;
    return fetch(url, { signal: controller.signal, ...options })
        .then((response) => {
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
        .then((response) => process(response))
        .catch((e) => {
            if (e.name === "AbortError") {
                console.log("Request aborted", fetchDescription);
                return undefined;
            } else {
                throw e;
            }
        });
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
            doPatch(url, updates).then(
                (response) =>
                    response && setData((prev) => ({ ...prev, ...response }))
            );
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
};
