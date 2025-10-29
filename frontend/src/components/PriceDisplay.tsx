type PriceDisplayProps = {
  label: string;
  amount: number;
  size?: "small" | "large";
};

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

const PriceDisplay = ({ label, amount, size = "small" }: PriceDisplayProps) => {
  const textSize = size === "large" ? "text-4xl" : "text-xl";
  const labelSize = size === "large" ? "text-sm" : "text-xs";

  return (
    <div>
      <p className={`text-gray-500 dark:text-gray-400 mb-1 ${labelSize}`}>
        {label}
      </p>
      <p className={`font-semibold text-gray-800 dark:text-white ${textSize}`}>
        {formatCurrency(amount)}
      </p>
    </div>
  );
};

export default PriceDisplay;

