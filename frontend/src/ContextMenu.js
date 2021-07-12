import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import useWindowDimensions from "./WindowDimensions";
import { TLink } from "./Util";

const ShowContextMenu = React.createContext();

function ContextMenu(props) {
    const hidden = { x: 0, y: 0, top: 0, left: 0, entries: [] };
    const pad = 10;
    const node = useRef();
    const [state, setState] = useState(hidden);
    const { width, height } = useWindowDimensions();

    function handleClick(e) {
        if (node.current && node.current.contains(e.target)) return;
        setState(hidden);
    }

    useEffect(() => {
        document.addEventListener("mousedown", handleClick);
        return () => {
            document.removeEventListener("mousedown", handleClick);
        };
    });

    useEffect(() => {
        if (node.current) {
            const w = node.current.offsetWidth;
            const h = node.current.offsetHeight;
            setState({
                x: state.x,
                y: state.y,
                top: state.y + h + pad > height ? height - h - pad : state.y,
                left: state.x + w + pad > width ? width - w - pad : state.x,
                entries: state.entries,
            });
        }
    }, [width, height, state.entries, state.x, state.y]);

    function showContextMenu(event, entries) {
        entries = entries.filter((x) => x);
        if (entries.length && window.getSelection().toString().length === 0) {
            setState({
                entries,
                y: event.clientY,
                x: event.clientX,
                top: 0,
                left: 0,
            });
            event.preventDefault();
        }
    }

    const divStyle = {
        left: state.left,
        top: state.top,
        visibility: state.left + state.top === 0 ? "hidden" : "visible",
    };

    return (
        <ShowContextMenu.Provider value={showContextMenu}>
            {props.children}
            {state.entries.length ? (
                <div ref={node} className="ContextMenu" style={divStyle}>
                    {state.entries.map((entry) => (
                        <p key={entry.name}>
                            <TLink
                                onClick={() => {
                                    entry.fn();
                                    setState(hidden);
                                }}
                            >
                                {entry.name}
                            </TLink>
                        </p>
                    ))}
                </div>
            ) : null}
        </ShowContextMenu.Provider>
    );
}

export { ContextMenu, ShowContextMenu };
