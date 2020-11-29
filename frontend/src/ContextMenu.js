import React, { useState, useEffect } from "react";

const ShowContextMenu = React.createContext();

function ContextMenu(props) {
    return (
        <ShowContextMenu.Provider value="hello">
            {props.children}
        </ShowContextMenu.Provider>
    );
}

export { ContextMenu, ShowContextMenu };
