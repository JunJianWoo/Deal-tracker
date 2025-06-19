import { ItemPriceData } from "../api/items";

interface OrderMethod {
  name: string;
  compareFn?: (arg1: ItemPriceData, arg2: ItemPriceData) => number;
}

interface OrderMethodCollection {
  [key: string]: OrderMethod;
}

const ORDER_METHODS: OrderMethodCollection = {
  "1": {
    "name": "Alphabetical (A → Z)",
    "compareFn": (a, b) => {
      return a.name
        .toLocaleLowerCase()
        .localeCompare(b.name.toLocaleLowerCase());
    },
  },
  "2": {
    "name": "Price (Low → High)",
    "compareFn": (a, b) => {
      return a.discountedPrice - b.discountedPrice;
    },
  },
  "3": {
    "name": "Price (High → Low)",
    "compareFn": (a, b) => {
      return b.discountedPrice - a.discountedPrice;
    },
  },
  "4": {
    "name": "Discount Amount (High → Low)",
    "compareFn": (a, b) => {
      return (
        b.originalPrice -
        b.discountedPrice -
        (a.originalPrice - a.discountedPrice)
      );
    },
  },
  "5": {
    "name": "Discount Percent (High → Low)",
    "compareFn": (a, b) => {
      return (
        a.discountedPrice / a.originalPrice -
        b.discountedPrice / b.originalPrice
      );
    },
  },
};

function longestOrderString(orderMethod: OrderMethodCollection) {
  return Object.entries(orderMethod)
    .map(([_, value]) => {
      return value.name;
    })
    .reduce((max, currentValue) => {
      return currentValue.length > max.length ? currentValue : max;
    }, "");
}

export { ORDER_METHODS, longestOrderString };
