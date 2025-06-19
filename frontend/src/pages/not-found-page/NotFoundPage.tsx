import "./NotFoundPage.css";
import Navbar from "../../components/navbar/Navbar";

function NotFoundPage() {
  return (
    <>
      <Navbar />
      <div className="not-found-text">
        <span>404 Not Found</span>
      </div>
    </>
  );
}

export default NotFoundPage;
