import React, { useState, useEffect } from "react";
import "./App.css";
import Cookies from "js-cookie";
let controller;
let fetchDescription;

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
        .then((response) => process(response))
        .catch((e) => {
            if (e.name === "AbortError") {
                console.log("request aborted", fetchDescription);
                return {};
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

function useData(url) {
    const [data, setData] = useState();
    useEffect(() => {
        doGet(url).then((response) => setData(response));
    }, [url]);
    return [
        data,
        (updates) => {
            setData((prev) => ({ ...prev, ...updates }));
            doPatch(url, updates).then((response) =>
                setData((prev) => ({ ...prev, ...response }))
            );
        },
    ];
}

export { TLink, SLink, doPatch, doGet, doDelete, useData };
