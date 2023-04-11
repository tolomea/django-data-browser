import React, { useState } from "react";

const GetCurrentSavedView = React.createContext();
const SetCurrentSavedView = React.createContext();

function CurrentSavedView(props) {
    const [state, setState] = useState(null);

    return (
        <GetCurrentSavedView.Provider value={state}>
            <SetCurrentSavedView.Provider value={setState}>
                {props.children}
            </SetCurrentSavedView.Provider>
        </GetCurrentSavedView.Provider>
    );
}

export { CurrentSavedView, GetCurrentSavedView, SetCurrentSavedView };
