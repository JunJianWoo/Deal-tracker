import "./Navbar.css";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Navbar as BSNavBar, Nav, Container } from "react-bootstrap";
import { useState } from "react";
import { Link } from "react-router-dom";
import { fetchDealsToday } from "../../api/items";
import Spinner from "react-bootstrap/Spinner";
import DismissibleAlert from "../dismissible-alert/DismissibleAlert";

function Navbar() {
  const queryClient = useQueryClient();
  const [isFetchLoading, setFetchLoading] = useState(false);
  const [showAlert, setShowAlert] = useState(false);

  const { mutateAsync: fetchDealsMutation } = useMutation({
    mutationFn: fetchDealsToday,
    onSuccess: (response) => {
      if (response.status == 304) {
        setShowAlert(true);
      }
      queryClient.invalidateQueries({ queryKey: ["getCurrentDeals"] });
      setFetchLoading(false);
    },
  });

  const fetchDeals = () => {
    setFetchLoading(true);

    fetchDealsMutation();
  };

  return (
    <>
      <BSNavBar sticky="top">
        <Container fluid>
          <Nav>
            <Nav.Item>
              <Link className="nav-link" to="/">
                Home
              </Link>
            </Nav.Item>
          </Nav>
          <Nav className="ms-auto">
            <Nav.Item>
              {isFetchLoading ? (
                <Spinner animation="border" role="status" variant="light" />
              ) : (
                <Container className="fetch-container" onClick={fetchDeals}>
                  <svg className="fetch-icon" viewBox="0 0 24 24">
                    <path
                      d="M17 17H17.01M17.4 14H18C18.9319 14 19.3978 14 19.7654 14.1522C20.2554 14.3552 20.6448 14.7446 20.8478 15.2346C21 15.6022 21 16.0681 21 17C21 17.9319 21 18.3978 20.8478 18.7654C20.6448 19.2554 20.2554 19.6448 19.7654 19.8478C19.3978 20 18.9319 20 18 20H6C5.06812 20 4.60218 20 4.23463 19.8478C3.74458 19.6448 3.35523 19.2554 3.15224 18.7654C3 18.3978 3 17.9319 3 17C3 16.0681 3 15.6022 3.15224 15.2346C3.35523 14.7446 3.74458 14.3552 4.23463 14.1522C4.60218 14 5.06812 14 6 14H6.6M12 15V4M12 15L9 12M12 15L15 12"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                  <span className="fetch-text">
                    Fetch <br />
                    Deals
                  </span>
                </Container>
              )}
            </Nav.Item>
          </Nav>
        </Container>
      </BSNavBar>
      <DismissibleAlert
        message="Already fetched deals today"
        showAlert={showAlert}
        setShowAlert={setShowAlert}
      />
    </>
  );
}

export default Navbar;
