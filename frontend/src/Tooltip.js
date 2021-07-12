import React, { useState, useRef } from "react";
import "./App.css";
import useWindowDimensions from "./WindowDimensions";
const ShowTooltip = React.createContext();
const HideTooltip = React.createContext();

function Tooltip(props) {
    const hidden = { left: 0, top: 0, messages: [] };
    const pad = 10;
    const minWidth = 200;
    const node = useRef();
    const [state, setState] = useState(hidden);
    const { width } = useWindowDimensions();

    function showTooltip(event, messages) {
        if (messages) {
            var left = event.target.getBoundingClientRect().right;
            var top = event.target.getBoundingClientRect().top - pad;
            if (left + minWidth > width) {
                left = width - minWidth;
                top = event.target.getBoundingClientRect().bottom;
            }
            setState({ messages, left, top });
        }
        event.preventDefault();
    }

    function hideTooltip(event) {
        setState(hidden);
        event.preventDefault();
    }

    const divStyle = { left: state.left, top: state.top };

    return (
        <ShowTooltip.Provider value={showTooltip}>
            <HideTooltip.Provider value={hideTooltip}>
                {props.children}
                {state.messages.length ? (
                    <div ref={node} className="Tooltip" style={divStyle}>
                        {state.messages.map((m) => (
                            <p>{m}</p>
                        ))}
                    </div>
                ) : null}
            </HideTooltip.Provider>
        </ShowTooltip.Provider>
    );
}

export { Tooltip, ShowTooltip, HideTooltip };
