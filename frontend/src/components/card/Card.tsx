import "./Card.css";
import { Card as BSCard } from "react-bootstrap";

interface Props {
  item: Item;
}

interface Item {
  id: string;
  name: string;
  imageLink: string;
  websiteLink: string;
  companySource: string;
  date: string;
  discountedPrice: number;
  originalPrice: number;
}

function Card({ item }: Props) {
  return (
    <BSCard>
      <a href={item.websiteLink} target="_blank" style={{ display: "grid" }}>
        <BSCard.Img src={item.imageLink} />
      </a>
      <BSCard.Body>
        <a href={item.websiteLink} target="_blank">
          <BSCard.Title>{item.name}</BSCard.Title>
        </a>
      </BSCard.Body>
      <div className="card-price">
        <div className="new-price ">
          <span className="currency">$</span>
          <span>{item.discountedPrice}</span>
        </div>
        <div className="old-price">$ {item.originalPrice}</div>
        <div className="discount">
          ${item.originalPrice - item.discountedPrice} Off
        </div>
      </div>
    </BSCard>
  );
}

export type { Item };
export default Card;
