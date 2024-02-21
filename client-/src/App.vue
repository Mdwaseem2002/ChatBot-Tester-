<template>
    <div class="container">
      <div class="chat-heading">
        <h2>CHAT TESTER</h2>
      </div>
  
      <div class="input-section">
        <textarea v-model="textInput" placeholder="Enter text" class="input-textarea" rows="5"></textarea>
      </div>
  
      <div class="test-case-selection">
        <label for="test-case-type">Test Case Type:</label>
        <select v-model="testCaseType" id="test-case-type">
          <option value="Type A">Type A</option>
          <option value="Type B">Type B</option>
          <!-- Add more options as needed -->
        </select>
      </div>
  
      <div class="error-classification">
        <label for="error-type">Error Classification:</label>
        <select v-model="errorType" id="error-type">
          <option value="Syntax Error">Syntax Error</option>
          <option value="Runtime Error">Runtime Error</option>
          <!-- Add more options as needed -->
        </select>
      </div>
  
      <div class="generate-section">
        <button @click="generateContent" class="generate-button">Generate</button>
      </div>
  
      <!-- <div v-if="generatedContent || errorMessage" class="result-section">
        <div class="generated-content-box" v-if="generatedContent">
          <h3>OUTPUT</h3>
          <ul>
            <li v-for="(point, index) in generatedContent" :key="index">
              <span :class="{ 'bigger-font': point.startsWith('*') }">{{ point }}</span>
            </li>
          </ul>
        </div>
        <div v-if="errorMessage" class="error-section">
          <p>Error: {{ errorMessage }}</p>
        </div>
      </div> -->
      <div v-html="markdownOutput"> </div>
    </div>
  </template>
  
  <script>

  import showdown from 'showdown';

  export default {
    data() {
      return {
        textInput: "",
        generatedContent: [],
        errorMessage: "",
        testCaseType: "",
        errorType: "",
        markdownOutput: "",
      };
    },
    methods: {
      async generateContent() {
        try {
          const response = await fetch('http://127.0.0.1:5000/generate_content', {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
              text: this.textInput,
              testCaseType: this.testCaseType,
              errorType: this.errorType
            })
          });
  
          const responseData = await response.json();
  
          if (response.ok) {
            console.log(responseData)
            
            this.markdownOutput = this.converter.makeHtml(responseData.generated_content)
            
            this.generatedContent = responseData.generated_content.split('\n');
            this.errorMessage = "";
          } else {
            this.generatedContent = [];
            this.errorMessage = responseData.message || "Failed to generate content.";
          }
        } catch (error) {
          console.error("Error generating content:", error);
          this.generatedContent = [];
          this.errorMessage = "An error occurred while generating content.";
        }
      }
    },
    mounted() {
      this.converter = new showdown.Converter();
    }
  };
  </script>
  
  <style>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: sans-serif;
    background-color:whitesmoke; /* Changed background color to light grey */
    padding: 2rem;
  }
  
  .chat-heading {
    margin-top: 20px;
    text-align: center;
  }
  
  h2 {
    font-size: 28px;
    color: #449D44;
  }
  
  .input-section,
  .generate-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
    margin-bottom: 20px;
    width: 100%;
    height: 250px;
  }
  
  .input-textarea {
    flex: 1;
    width: 1500px;
    min-height: 100px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    resize: horizontal;
    margin-right: 10px;
  }
  
  .test-case-selection label,
  .error-classification label {
    margin-bottom: 5px; /* Adjusted for better spacing */
  }
  
  .test-case-selection select,
  .error-classification select {
    width: 600px;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .generate-button {
    margin-top: 10px; /* Adjusted for better spacing */
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .generate-button:hover {
    background-color: #0056b3;
  }
  
  .result-section,
  .error-section {
    text-align: center;
    max-width: 80%;
    margin-bottom: 20px;
  }
  
  .generated-content-box {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
    width: 1500px; /* Same width as input textarea */
    max-width: 100%;
    min-height: 100%;
    margin: 20px auto; /* Center horizontally and vertically */
    text-align: left; /* Align text to start from the left */
  }
  
  .bold {
    font-weight: bo;
  }
  
  p {
    font-size: 18px;
    color: #333;
  }
  
  .bigger-font{
    font-size: 20px;
  }
  </style>
  