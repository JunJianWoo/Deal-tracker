import "./Grid.css";
import { Item } from "../card/Card";
import Card from "../card/Card";
import { useState } from "react";
import PaginationBar from "../pagination-bar/PaginationBar";
import { Container, Row, Col } from "react-bootstrap";

interface Props {
  items: Item[];
}

function Grid({ items }: Props) {
  const PAGE_SIZE = 60;
  const [pageNumber, setPageNumber] = useState(1);
  const maxPages = Math.max(Math.ceil(items.length / PAGE_SIZE), 1);

  const getInPageItems = (pageNo: number) => {
    let item_lst = [];
    for (
      let i = (pageNo - 1) * PAGE_SIZE;
      i < pageNo * PAGE_SIZE && i < items.length;
      i++
    ) {
      item_lst.push(items[i]);
    }
    return item_lst;
  };

  return (
    <>
      <Container className="card-container">
        <Row>
          {getInPageItems(pageNumber).map((item) => {
            return (
              <Col sm={5} md={4} lg={3} className="column">
                <Card item={item}></Card>
              </Col>
            );
          })}
        </Row>
        <Col className="page-holder">
          <div className="item-count">
            Showing {(pageNumber - 1) * PAGE_SIZE + (items.length == 0 ? 0 : 1)}{" "}
            - {pageNumber == maxPages ? items.length : pageNumber * PAGE_SIZE}{" "}
            of {items.length} items
          </div>
          <PaginationBar
            currentPage={pageNumber}
            maxPages={maxPages}
            handlePageChange={(x) => setPageNumber(x)}
          />
        </Col>
      </Container>
    </>
  );
}

export default Grid;
