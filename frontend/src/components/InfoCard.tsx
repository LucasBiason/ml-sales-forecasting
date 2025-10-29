type InfoCardProps = {
  label: string;
  value: string | number;
};

const InfoCard = ({ label, value }: InfoCardProps) => {
  return (
    <div className="bg-gray-50 dark:bg-gray-700/50 rounded p-3">
      <p className="text-gray-500 dark:text-gray-400 mb-1 text-xs">{label}</p>
      <p className="font-semibold text-gray-800 dark:text-white">{value}</p>
    </div>
  );
};

export default InfoCard;

