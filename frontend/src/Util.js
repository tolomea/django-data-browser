import React from "react";
import "./App.css";
import Cookies from "js-cookie";
let controller;

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

function fetch_wrap(url, config) {
    if (controller) controller.abort();
    controller = new AbortController();
    return fetch(url, { signal: controller.signal, ...config })
        .then((response) => response.json())
        .catch((e) => {
            if (e.name === "AbortError") {
                console.log("request aborted");
                return {};
            } else {
                throw e;
            }
        });
}

function get(url) {
    return fetch_wrap(url);
}

function patch(url, data) {
    return fetch_wrap(url, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(data),
    });
}

export { TLink, SLink, patch, get };
