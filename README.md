# Smart Grocery - AI-Powered Recipe and Nutrition Assistant

Smart Grocery is an intelligent recipe recommendation system that helps users create healthy Indian recipes based on their nutritional requirements. The application combines machine learning, natural language processing, and nutritional analysis to suggest personalized recipes and provide detailed nutritional information.

## Features

- **Nutritional Analysis**: Uses a Decision Tree model to analyze and predict nutritional content
- **Recipe Generation**: Leverages Google's Gemma model to create authentic Indian recipes
- **Ingredient Smart Selection**: Intelligently processes and selects ingredients based on nutritional requirements
- **Comprehensive Nutrition Tracking**: Provides detailed breakdown of various nutrients including calories, proteins, carbs, vitamins, and minerals

## Workflow

1. **Nutritional Input**
   - User provides their nutritional requirements
   - System processes these requirements using a trained Decision Tree model
   - Nutritional parameters analyzed include calories, protein, carbs, fats, vitamins, and minerals

2. **Ingredient Selection**
   - System searches through a comprehensive food database
   - Selects ingredients that match the nutritional requirements
   - Cleans and processes ingredient names for better recipe generation
   - Filters out brand names and irrelevant information

3. **Recipe Generation**
   - Selected ingredients are passed to the Gemma 2B model
   - Model generates authentic Indian recipes
   - Includes:
     - Dish name
     - Regional cuisine type
     - Complete ingredient list
     - Step-by-step cooking instructions
     - Preparation and cooking time

4. **Nutritional Summary**
   - Calculates total nutritional content of the suggested recipe
   - Provides detailed breakdown of all nutrients
   - Ensures alignment with user's nutritional goals

## Technology Stack

- **Frontend**: Streamlit
- **AI Models**:
  - Google Gemini 2.0 Flash (for prompting)
  - Gemma 2B (for recipe generation)
  - Custom Decision Tree model (for nutrition prediction)
- **Data Processing**: Pandas, NumPy
- **API Integration**: HuggingFace Inference API

## Getting Started

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your API keys in Streamlit secrets:
   - Gemini API key
   - HuggingFace API key

3. Run the application:
   ```bash
   streamlit run main.py
   ```

## Project Structure

```
Smart Grocery/
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
├── Models/             
│   └── Nutrition_model_Decision_tree.pkl  # Trained nutrition model
└── synthetic_health_data.csv  # Training/reference data
```

## Note

This project uses AI models to generate recipes and should be used as a guideline. Always verify nutritional information and recipe suitability based on your specific dietary needs and restrictions.