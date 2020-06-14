import React from "react";
import "./App.css";

function Link(props) {
    return (
        <button
            type="button"
            className={"Link " + (props.className || "")}
            onClick={props.onClick}
        >
            {props.children}
        </button>
    );
}

function SLink(props) {
    return (
        <button
            type="button"
            className={"sLink material-icons " + (props.className || "")}
            onClick={props.onClick}
        >
            {props.children}
        </button>
    );
}

export { Link, SLink };
