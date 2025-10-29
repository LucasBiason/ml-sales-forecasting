export type PropertyType = "D" | "S" | "T" | "F" | "O";
export type OldNew = "Y" | "N";
export type Duration = "F" | "L" | "U";

export type PropertyInput = {
  property_type: PropertyType;
  old_new: OldNew;
  duration: Duration;
  county: string;
  postcode: string;
  year: number;
};

export type ConfidenceInterval = {
  min: number;
  max: number;
};

export type ModelInfo = {
  type: string;
  n_estimators: number;
  expected_r2: number;
};

export type PredictionResponse = {
  predicted_price: number;
  confidence_interval: ConfidenceInterval;
  features_used: string[];
  model_info: ModelInfo;
};

export type HealthResponse = {
  status: string;
  timestamp: string;
  model_loaded: boolean;
  version: string;
};

