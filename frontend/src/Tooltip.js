import React, { useState, useRef } from "react";
import "./App.css";
import useWindowDimensions from "./WindowDimensions";
const ShowTooltip = React.createContext();
const HideTooltip = React.createContext();

function Tooltip(props) {
    const node = useRef();
    const [state, setState] = useState();
    const { width } = useWindowDimensions();

    const divStyle = state
        ? {
              left: state.x,
              top: state.y,
          }
        : {};

    function showTooltip(event, messages) {
        if (messages) {
            var x = event.target.getBoundingClientRect().right;
            var y = event.target.getBoundingClientRect().top - 10;
            if (x + 200 > width) {
                x = width - 200;
                y = event.target.getBoundingClientRect().bottom;
            }

            setState({
                messages: messages,
                x: x,
                y: y,
            });
        }
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
