import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import { TLink } from "./Util";

const ShowContextMenu = React.createContext();

function ContextMenu(props) {
    const node = useRef();
    const [state, setState] = useState();

    function handleClick(e) {
        if (node.current && node.current.contains(e.target)) return;
        setState(null);
    }

    useEffect(() => {
        document.addEventListener("mousedown", handleClick);
        return () => {
            document.removeEventListener("mousedown", handleClick);
        };
    }, []);

    const divStyle = state
        ? {
              left: state.x,
              top: state.y,
          }
        : {};

    function showContextMenu(event, entries) {
        entries = entries.filter((x) => x);
        if (entries.length) {
            setState({
                entries: entries,
                x: event.clientX,
                y: event.clientY,
            });
            event.preventDefault();
        }
    }

    return (
        <ShowContextMenu.Provider value={showContextMenu}>
            {props.children}
            {state && (
                <div ref={node} className="ContextMenu" style={divStyle}>
                    {state.entries.map((entry) => (
                        <p key={entry.name}>
                            <TLink
                                onClick={() => {
                                    entry.fn();
                                    setState();
                                }}
                            >
                                {entry.name}
                            </TLink>
                        </p>
                    ))}
                </div>
            )}
        </ShowContextMenu.Provider>
    );
}

export { ContextMenu, ShowContextMenu };
