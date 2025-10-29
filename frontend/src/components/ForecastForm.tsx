import { useState } from "react";
import { Home, Calendar, MapPin, Building2 } from "lucide-react";
import type { PropertyInput } from "../types";

type ForecastFormProps = {
  onSubmit: (data: PropertyInput) => void;
  loading: boolean;
};

const ForecastForm = ({ onSubmit, loading }: ForecastFormProps) => {
  const [formData, setFormData] = useState<PropertyInput>({
    property_type: "T",
    old_new: "N",
    duration: "F",
    county: "",
    postcode: "",
    year: new Date().getFullYear(),
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "year" ? parseInt(value) : value.toUpperCase(),
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <div className="flex items-center gap-3 mb-6">
        <Home className="w-8 h-8 text-blue-600" />
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
          Property Details
        </h2>
      </div>

      {/* Property Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <Building2 className="w-4 h-4 inline mr-2" />
          Property Type
        </label>
        <select
          name="property_type"
          value={formData.property_type}
          onChange={handleChange}
          className="input-field"
          required
        >
          <option value="D">Detached</option>
          <option value="S">Semi-detached</option>
          <option value="T">Terraced</option>
          <option value="F">Flat</option>
          <option value="O">Other</option>
        </select>
      </div>

      {/* Old/New */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Property Condition
        </label>
        <select
          name="old_new"
          value={formData.old_new}
          onChange={handleChange}
          className="input-field"
          required
        >
          <option value="N">Existing</option>
          <option value="Y">New Build</option>
        </select>
      </div>

      {/* Duration */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Tenure Type
        </label>
        <select
          name="duration"
          value={formData.duration}
          onChange={handleChange}
          className="input-field"
          required
        >
          <option value="F">Freehold</option>
          <option value="L">Leasehold</option>
          <option value="U">Unknown</option>
        </select>
      </div>

      {/* County */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <MapPin className="w-4 h-4 inline mr-2" />
          County
        </label>
        <input
          type="text"
          name="county"
          value={formData.county}
          onChange={handleChange}
          placeholder="e.g. GREATER LONDON"
          className="input-field"
          required
          minLength={2}
          maxLength={50}
        />
      </div>

      {/* Postcode */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Postcode
        </label>
        <input
          type="text"
          name="postcode"
          value={formData.postcode}
          onChange={handleChange}
          placeholder="e.g. SW1A 1AA"
          className="input-field"
          required
          minLength={5}
          maxLength={10}
        />
      </div>

      {/* Year */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <Calendar className="w-4 h-4 inline mr-2" />
          Sale Year
        </label>
        <input
          type="number"
          name="year"
          value={formData.year}
          onChange={handleChange}
          className="input-field"
          required
          min={1995}
          max={2030}
        />
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="btn-primary w-full py-3 text-lg"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Predicting...
          </span>
        ) : (
          "Predict Price"
        )}
      </button>
    </form>
  );
};

export default ForecastForm;

