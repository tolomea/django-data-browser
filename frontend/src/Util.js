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

export { Link };
