import { useParams } from "react-router-dom";

function SearchPage() {
  const params = useParams<{ itemName: string }>();

  return <div>{params.itemName}</div>;
}

export default SearchPage;
