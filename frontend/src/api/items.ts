interface ItemPriceData {
  id: string;
  name: string;
  imageLink: string;
  websiteLink: string;
  companySource: string;
  date: string;
  originalPrice: number;
  discountedPrice: number;
}

interface FilterArguments {
  [key: string]: string[] | Number;
}

async function getCurrentDeals(body: FilterArguments) {
  const response = await fetch(import.meta.env.VITE_API_URL + "/dealstoday", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return await response.json();
}

async function fetchDealsToday() {
  const response = await fetch(import.meta.env.VITE_API_URL + "/fetchdeals", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  // Jsonify response only if successful
  if (response.status == 200) {
    return await response.json();
  }
  return response;
}

export type { ItemPriceData, FilterArguments };
export { getCurrentDeals, fetchDealsToday };
