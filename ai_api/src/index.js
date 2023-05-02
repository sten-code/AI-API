import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout"
import HomePage from "./pages/HomePage";
import TextGen from "./pages/TextGen";
import ImageGen from "./pages/ImageGen";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="TextGen" element={<TextGen />} />
          <Route path="ImageGen" element={<ImageGen />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));

