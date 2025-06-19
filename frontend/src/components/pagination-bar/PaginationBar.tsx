import "./PaginationBar.css";
import { findPageNumber } from "../../utils/util";
import Pagination from "react-bootstrap/Pagination";

interface Props {
  currentPage: number;
  maxPages: number;
  handlePageChange: (x: number) => void;
}
function PaginationBar({ currentPage, handlePageChange, maxPages }: Props) {
  let possiblePages = findPageNumber(maxPages, currentPage, 5);

  return (
    <Pagination>
      <Pagination.First
        disabled={currentPage == 1}
        onClick={() => {
          handlePageChange(1);
        }}
        linkClassName="direction"
      />

      {possiblePages.map((pageNo) => {
        return (
          <Pagination.Item
            active={currentPage == pageNo}
            onClick={() => {
              handlePageChange(pageNo);
            }}
          >
            {pageNo}
          </Pagination.Item>
        );
      })}

      <Pagination.Last
        disabled={currentPage == maxPages}
        onClick={() => {
          handlePageChange(maxPages);
        }}
        linkClassName="direction"
      />
    </Pagination>
  );
}

export default PaginationBar;
