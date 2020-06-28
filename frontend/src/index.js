import React from "react";
import ReactDOM from "react-dom";
import * as Sentry from "@sentry/browser";
import "./index.css";
import App from "./App";

const config = JSON.parse(
    document.getElementById("backend-config").textContent
);
const version = document.getElementById("backend-version").textContent.trim();

if (config.sentryDsn) {
    Sentry.init({
        dsn: config.sentryDsn,
        release: version,
        attachStacktrace: true,
        maxValueLength: 10000,
    });
}

ReactDOM.render(
    <React.StrictMode>
        <App {...config} />
    </React.StrictMode>,
    document.getElementById("root")
);
