import React, { createContext, useState } from "react";

export const NavigationContext = createContext();

export const NavigationProvider = ({ children }) => {
  const [currentScreen, setCurrentScreen] = useState("");
  const [fromLanguages, setFromLanguages] = useState([]);
  const [toLanguages, setToLanguages] = useState([]);
  let langOne = [];
  let langTwo = [];
  return (
    <NavigationContext.Provider
      value={{
        currentScreen,
        setCurrentScreen,
        fromLanguages,
        setFromLanguages,
        toLanguages,
        setToLanguages,
        langOne,
        langTwo,
      }}
    >
      {children}
    </NavigationContext.Provider>
  );
};
