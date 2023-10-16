import * as React from "react";
import Routes from "./routes/route";
import { NavigationProvider } from "./context/NavigationContext";

export default function App() {
 
  return (
    <NavigationProvider>
      <Routes />
    </NavigationProvider>
  );
}





