import "./DismissibleAlert.css";
import { Alert } from "react-bootstrap";

interface Props {
  message: string;
  showAlert: boolean;
  setShowAlert: (x: boolean) => void;
}

function DismissibleAlert({ message, showAlert, setShowAlert }: Props) {
  // Autodismiss
  if (showAlert) {
    setTimeout(() => setShowAlert(false), 3000);
  }

  return (
    <Alert
      show={showAlert}
      variant="secondary"
      onClose={() => {
        setShowAlert(false);
      }}
      transition={true}
      dismissible
    >
      {message}
    </Alert>
  );
}

export default DismissibleAlert;
