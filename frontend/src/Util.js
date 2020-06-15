import React from "react";
import "./App.css";

function Link(props) {
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

export { Link, SLink };
