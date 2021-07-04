import React, { useState, useRef } from "react";
import "./App.css";

const ShowTooltip = React.createContext();
const HideTooltip = React.createContext();

function Tooltip(props) {
    const node = useRef();
    const [state, setState] = useState();

    const divStyle = state
        ? {
              left: state.x,
              top: state.y,
          }
        : {};

    function showTooltip(event, messages) {
        if (messages)
            setState({
                messages: messages,
                x: event.target.getBoundingClientRect().right,
                y: event.target.getBoundingClientRect().top - 10,
            });
        event.preventDefault();
    }

    function hideTooltip(event) {
        setState(null);
        event.preventDefault();
    }

    return (
        <ShowTooltip.Provider value={showTooltip}>
            <HideTooltip.Provider value={hideTooltip}>
                {props.children}
                {state && (
                    <div ref={node} className="Tooltip" style={divStyle}>
                        {state.messages.map((m) => (
                            <p>{m}</p>
                        ))}
                    </div>
                )}
            </HideTooltip.Provider>
        </ShowTooltip.Provider>
    );
}

export { Tooltip, ShowTooltip, HideTooltip };
