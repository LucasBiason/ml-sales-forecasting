import { TrendingUp, AlertCircle, Info } from "lucide-react";
import InfoCard from "./InfoCard";
import PriceDisplay from "./PriceDisplay";
import type { PredictionResponse } from "../types";

type ForecastResultProps = {
  result: PredictionResponse | null;
  error: string | null;
};

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

const ForecastResult = ({ result, error }: ForecastResultProps) => {
  if (error) {
    return (
      <div className="card bg-red-50 dark:bg-red-900/20 border-2 border-red-300 dark:border-red-700">
        <div className="flex items-start gap-3">
          <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-red-800 dark:text-red-300 mb-2">
              Prediction Error
            </h3>
            <p className="text-red-700 dark:text-red-400">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const rangeSpread =
    result.confidence_interval.max - result.confidence_interval.min;
  const percentageSpread =
    (rangeSpread / result.predicted_price) * 100;

  return (
    <div className="card">
      <div className="flex items-center gap-3 mb-6">
        <TrendingUp className="w-8 h-8 text-green-600" />
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Prediction Result
        </h2>
      </div>

      {/* Predicted Price */}
      <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/30 rounded-lg p-6 mb-6">
        <PriceDisplay
          label="Predicted Price"
          amount={result.predicted_price}
          size="large"
        />
      </div>

      {/* Confidence Interval */}
      <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Info className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Confidence Interval (80%)
          </p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <PriceDisplay
            label="Minimum"
            amount={result.confidence_interval.min}
          />
          <PriceDisplay
            label="Maximum"
            amount={result.confidence_interval.max}
          />
        </div>
        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Range: {formatCurrency(rangeSpread)} (±{percentageSpread.toFixed(1)}%)
          </p>
        </div>
      </div>

      {/* Model Info */}
      <div className="grid grid-cols-2 gap-4 text-sm">
        <InfoCard label="Model" value={result.model_info.type} />
        <InfoCard label="Trees" value={result.model_info.n_estimators} />
        <InfoCard
          label="Expected R²"
          value={`${(result.model_info.expected_r2 * 100).toFixed(2)}%`}
        />
        <InfoCard label="Features" value={result.features_used.length} />
      </div>
    </div>
  );
};

export default ForecastResult;

