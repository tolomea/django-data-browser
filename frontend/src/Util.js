import React, { useState, useRef, useContext } from "react";
import { Redirect } from "react-router-dom";

import { ShowTooltip, HideTooltip } from "./Tooltip";
import { doPost, doPatch, doDelete } from "./Network";

import "./App.scss";

function CopyText(props) {
    const { text } = props;
    const ref = useRef(null);
    return (
        <>
            <span ref={ref}>{text}</span>{" "}
            <TLink
                className="CopyToClipboard"
                onClick={(event) => {
                    const range = document.createRange();
                    range.selectNodeContents(ref.current);
                    window.getSelection().removeAllRanges();
                    window.getSelection().addRange(range);
                    document.execCommand("copy");
                    window.getSelection().removeAllRanges();
                    event.target.blur();
                }}
            >
                (copy to clipboard)
            </TLink>
        </>
    );
}

function TLink(props) {
    const { className, onClick, children } = props;
    return (
        <button {...{ onClick }} type="button" className={`TLink ${className}`}>
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
            className={`SLink material-icons ${className}`}
        >
            {children}
        </button>
    );
}

function Save(props) {
    const { name, apiUrl, data, redirectUrl } = props;
    const [state, setState] = useState("save");
    if (state === "save")
        return (
            <TLink
                onClick={(event) => {
                    setState("saving");
                    doPost(apiUrl, data).then((response) => setState(response));
                }}
            >
                Save {name || ""}
            </TLink>
        );
    else if (state === "saving") return <>Saving {name || ""}</>;
    else {
        const url =
            typeof redirectUrl === "function"
                ? redirectUrl(state) // state here is the save response
                : redirectUrl;
        return <Redirect to={url} />;
    }
}

const CONFIRM_PROMPT = "Are you sure?";
const CONFIRM_TIMEOUT = 1000;

function Update(props) {
    const { name, apiUrl, data, redirectUrl } = props;
    const [state, setState] = useState("initial");
    var timerID = null;
    if (state === "initial")
        return (
            <TLink
                onClick={(event) => {
                    timerID = setTimeout(
                        () => setState("initial"),
                        CONFIRM_TIMEOUT,
                    );
                    setState("confirm");
                }}
            >
                Update {name || ""}
            </TLink>
        );
    else if (state === "confirm")
        return (
            <TLink
                onClick={(event) => {
                    setState("updating");
                    if (timerID) {
                        clearTimeout(timerID);
                        timerID = null;
                    }
                    doPatch(apiUrl, data).then((response) =>
                        setState("updated"),
                    );
                }}
            >
                {CONFIRM_PROMPT}
            </TLink>
        );
    else if (state === "updating") return "Updating";
    else if (state === "updated") return <Redirect to={redirectUrl} />;
    else throw new Error(`unknown update state: ${state}`);
}

function Delete(props) {
    const { name, apiUrl, redirectUrl } = props;
    const [state, setState] = useState("initial");
    var timerID = null;
    if (state === "initial")
        return (
            <TLink
                onClick={(event) => {
                    timerID = setTimeout(
                        () => setState("initial"),
                        CONFIRM_TIMEOUT,
                    );
                    setState("confirm");
                }}
            >
                Delete {name || ""}
            </TLink>
        );
    else if (state === "confirm")
        return (
            <TLink
                onClick={(event) => {
                    setState("deleting");
                    if (timerID) {
                        clearTimeout(timerID);
                        timerID = null;
                    }
                    doDelete(apiUrl).then((response) => setState("deleted"));
                }}
            >
                {CONFIRM_PROMPT}
            </TLink>
        );
    else if (state === "deleting") return "Deleting";
    else if (state === "deleted") return <Redirect to={redirectUrl} />;
    else throw new Error(`unknown delete state: ${state}`);
}

function Overlay(props) {
    if (!props.message) return null;
    return (
        <div className="Overlay">
            <h1>{props.message}</h1>
        </div>
    );
}

function is(x: any, y: any) {
    return (
        (x === y && (x !== 0 || 1 / x === 1 / y)) || (x !== x && y !== y) // eslint-disable-line no-self-compare
    );
}
const hasOwnProperty = Object.prototype.hasOwnProperty;
function shallowEqual(objA: mixed, objB: mixed): boolean {
    if (is(objA, objB)) {
        return true;
    }

    if (
        typeof objA !== "object" ||
        objA === null ||
        typeof objB !== "object" ||
        objB === null
    ) {
        return false;
    }

    const keysA = Object.keys(objA);
    const keysB = Object.keys(objB);

    if (keysA.length !== keysB.length) {
        console.log("different keys", keysA, keysB);
        return false;
    }

    // Test for A's keys different from B.
    for (let i = 0; i < keysA.length; i++) {
        if (
            !hasOwnProperty.call(objB, keysA[i]) ||
            !is(objA[keysA[i]], objB[keysA[i]])
        ) {
            console.log(
                "different key",
                keysA[i],
                objA[keysA[i]],
                objB[keysA[i]],
            );
            return false;
        }
    }

    return true;
}

function HasActionIcon(props) {
    const { modelField, message } = props;
    const showTooltip = useContext(ShowTooltip);
    const hideTooltip = useContext(HideTooltip);

    if (modelField.actions.length) {
        return (
            <>
                <span> </span>
                <span
                    className="Symbol material-icons-outlined"
                    onMouseEnter={(e) => showTooltip(e, [message])}
                    onMouseLeave={(e) => hideTooltip(e)}
                >
                    build_circle
                </span>
            </>
        );
    } else {
        return "";
    }
}

function HasToManyIcon(props) {
    const { modelField, message } = props;
    const showTooltip = useContext(ShowTooltip);
    const hideTooltip = useContext(HideTooltip);

    if (modelField.toMany) {
        return (
            <>
                <span> </span>
                <span
                    onMouseEnter={(e) => showTooltip(e, [message])}
                    onMouseLeave={(e) => hideTooltip(e)}
                >
                    {"\u21f6"}
                </span>
            </>
        );
    } else {
        return "";
    }
}

function useToggle(initial = false) {
    const [toggled, setToggled] = useState(initial);

    const toggleLink = (
        <SLink
            className="ToggleLink"
            onClick={() => setToggled((toggled) => !toggled)}
        >
            {toggled ? "remove" : "add"}
        </SLink>
    );

    return [toggled, toggleLink];
}

function usePersistentToggle(storageKey = null, initial = false) {
    const blah = localStorage.getItem(storageKey)
        ? localStorage.getItem(storageKey) === "true"
        : initial;

    const [toggled, setToggled] = useState(blah);

    const toggleLink = (
        <SLink
            className="ToggleLink"
            onClick={() =>
                setToggled((toggled) => {
                    localStorage.setItem(storageKey, !toggled);
                    return !toggled;
                })
            }
        >
            {toggled ? "remove" : "add"}
        </SLink>
    );

    return [toggled, toggleLink];
}

function isSubsequence(sub, str) {
    let subIndex = 0;
    let strIndex = 0;

    while (strIndex < str.length && subIndex < sub.length) {
        if (sub[subIndex] === str[strIndex]) {
            subIndex++;
        }
        strIndex++;
    }

    // If subIndex is equal to the length of sub, then all characters are found
    return subIndex === sub.length;
}

function strMatch(pattern, ...strs) {
    pattern = pattern.replace(/\s+/g, ".*").toLowerCase();
    for (const str of strs) {
        const cleanStr = str.replace(/\s+/g, "").toLowerCase();
        if (cleanStr.match(pattern)) return true;
    }
    return false;
}

export {
    TLink,
    SLink,
    Save,
    Update,
    Delete,
    CopyText,
    Overlay,
    shallowEqual,
    HasActionIcon,
    HasToManyIcon,
    useToggle,
    usePersistentToggle,
    isSubsequence,
    strMatch,
};
