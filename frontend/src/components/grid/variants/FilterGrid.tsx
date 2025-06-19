import "./FilterGrid.css";
import { getCurrentDeals } from "../../../api/items";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Grid from "../Grid";
import { Button, Dropdown, Form, Collapse } from "react-bootstrap";
import { useEffect, useState } from "react";
import { ORDER_METHODS, longestOrderString } from "../../../utils/orderMethod";
import { COMPANY_SOURCES } from "../../../utils/filters";
import { FilterArguments } from "../../../api/items";

function FilterGrid() {
  const queryClient = useQueryClient();
  // Hooks initialisation
  const [orderMethodIdx, setOrderMethodIdx] = useState("1");

  let initialFilter: FilterArguments = {
    "companySource": COMPANY_SOURCES,
  };
  const [filterArgs, setFilterArgs] = useState(initialFilter);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["getCurrentDeals"],
    queryFn: () => getCurrentDeals(filterArgs),
  });

  const [items, setItems] = useState([]);
  const [showFilter, setShowFilter] = useState(true);

  const { mutate: filterDealsMutation } = useMutation({
    mutationFn: (body: FilterArguments) => getCurrentDeals(body),
    onSuccess: (newData) => {
      queryClient.setQueryData(["getCurrentDeals"], (_) => newData);
    },
  });

  useEffect(() => {
    if (data) {
      // data.sort(ORDER_METHODS[orderMethodIdx].compareFn);
      // setItems(data);
      handleSortMethodChange(orderMethodIdx);
    }
  }, [data]);

  // Change functions
  const handleSortMethodChange = (methodIdx: string) => {
    data.sort(ORDER_METHODS[methodIdx].compareFn);
    setItems(data);
    setOrderMethodIdx(methodIdx);
  };

  const handleFilterArgChange = (key: string, value: string) => {
    if (Array.isArray(filterArgs[key])) {
      // Handle i.e. add if not exists, delete if exists
      const oriArray = filterArgs[key] as string[];
      if (oriArray.every((element) => element != value)) oriArray.push(value);
      else {
        filterArgs.companySource = oriArray.filter(
          (element) => element != value
        );
      }
    } else {
      // Handle single value changes (delete if empty)
      if (value == "") delete filterArgs[key];
      else filterArgs[key] = Math.round(Number(value));
    }
    setFilterArgs(filterArgs);
    filterDealsMutation(filterArgs);
  };

  // Async query handling
  if (isError) {
    return <div className="alert alert-danger">Error fetching deals!</div>;
  }

  if (isLoading) {
    return (
      <div className="spinner">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="config-bar">
        <div className="total-item-count">{items.length} Items Today</div>
        <div className="filter-order-box">
          <Button
            className="me-2 mb-2"
            onClick={() => {
              setShowFilter(!showFilter);
            }}
          >
            Filter
          </Button>
          <Dropdown>
            <Dropdown.Toggle
              style={{
                minWidth: longestOrderString(ORDER_METHODS).length + "ch",
              }}
            >
              {ORDER_METHODS[orderMethodIdx].name}
            </Dropdown.Toggle>

            <Dropdown.Menu>
              {Object.entries(ORDER_METHODS).map(([key, value]) => {
                return (
                  <Dropdown.Item
                    active={key == orderMethodIdx}
                    onClick={() => handleSortMethodChange(key)}
                  >
                    {value.name}
                  </Dropdown.Item>
                );
              })}
            </Dropdown.Menu>
          </Dropdown>
        </div>
      </div>
      <div className="filter-grid">
        <Collapse in={showFilter} dimension="width">
          <div className="filter-box">
            <div className="filter-header">Company Sources</div>
            {COMPANY_SOURCES.map((company: string) => {
              return (
                <Form.Check
                  label={company}
                  onClick={() => {
                    handleFilterArgChange("companySource", company);
                  }}
                  checked={(filterArgs["companySource"] as string[]).some(
                    (element: string) => element == company
                  )}
                />
              );
            })}
            <div className="filter-header">Price Range</div>
            <div style={{ display: "flex" }}>
              <Form.Control
                aria-label="Min Amount"
                placeholder="Min"
                type="number"
                step="10"
                onChange={(event) => {
                  handleFilterArgChange("minPrice", event.target.value);
                }}
              />
              <div className="arrow-divider">→</div>
              <Form.Control
                aria-label="Max Amount"
                type="number"
                step="10"
                placeholder="Max"
                onChange={(event) => {
                  handleFilterArgChange("maxPrice", event.target.value);
                }}
              />
            </div>
          </div>
        </Collapse>
        <div className="items-box">
          <Grid items={items} />
        </div>
      </div>
    </>
  );
}

export default FilterGrid;
