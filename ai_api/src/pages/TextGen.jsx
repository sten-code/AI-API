import React, { Component } from 'react'
import '../css/TextGen.css'

const getBoolean = (targetvalue) => {
    if (targetvalue === "false") {
      return false;
    } else if (targetvalue === "true") {
      return true;
    } else if (!isNaN(Number(targetvalue))) {
      return Number(targetvalue);
    } else {
      return targetvalue;
    }
}

const getResult = async (jsonData) => { 
    const res = await fetch("http://127.0.0.1:5000/text-generation/generate", {
        method: 'POST',
        body: jsonData,
        headers: {
          'Content-Type': 'application/json'
        }
      })
    const data = await res.json();
    console.log(data)
    const generatedText = data.response[0].generated_text

    return generatedText
}

const modelOptions = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5000/models');
      const data = await res.json();
      const textGenerationModels = data['text-generation'];
      const options = textGenerationModels.map((a) => { 
        return ('<option name="' + a +'">' + a + "</option> "   ) 
      });
      return options.join(" ");
    } catch (error) {
      console.error(error);
      return "";
    }
  }
  

export class TextGen extends Component {
  constructor(props) {
    super(props)
  
    this.state = {
        do_sample: true,
        max_new_tokens: 200,
        temp: 0.8,
        seed: 42,
        prompt: "Wat is your question?",
        models: "",
        model: "gpt2",
        result: "Click on generate to create an answer, it may take some time!"
     }
  
 }

 async componentDidMount() {
    modelOptions().then((result) => {
        this.setState({models: result})
    });
  }

  changeHandler = (e) => {
    this.setState({[e.target.name]: getBoolean(e.target.value)})

    modelOptions().then((result) => {
        this.setState({models: result})
    });


  }

  submitHandler = e => { 
    e.preventDefault()
    const { prompt, do_sample, max_new_tokens, temp, model, seed} = this.state;
    const config = { max_new_tokens, do_sample, temp, seed};
    const data = { prompt, model, config };
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
    getResult(jsonData).then((resultg) => {
        this.setState({result: resultg})
    })

  }

  render() {
    const {do_sample, temp, max_new_tokens, prompt, models, model ,result, seed} = this.state

    return (
      <div>
        
        <form onSubmit={this.submitHandler} className="form" >
          
          <div className='config'>
            
            <div className='input_field'>
                Tokens: 
                <input type="number" name="max_new_tokens" min="10" max="10000" value={max_new_tokens} onChange={this.changeHandler} className='input-box'/>
            </div> 
            
            <div className='input_field'>
                Temp: 
                <input type="number" name="temp"  min="0.1" max="10" step="0.1"value={temp} onChange={this.changeHandler} className='input-box'/>
            </div>
            
            <div className='input_field'>
                Do Sample: 
                <select name="do_sample" value={do_sample} onChange={this.changeHandler} className='input-box'>
                    <option value="true">True</option>
                    <option value="false">False</option>
                </select>
            </div>
           
            <div className='input_field'>
                Model: 
                <select name="model" className='input-box' value={model} onChange={this.changeHandler}  dangerouslySetInnerHTML={{ __html: models }}></select>
            </div> 
            <div className='input_field'>
                Seed: 
                <input name="seed" className='input-box' value={seed} onChange={this.changeHandler} />
            </div> 
          
          </div><br></br>
          
          <div className='ask'>
            <textarea type="text" className="question" name="prompt" value={prompt} onChange={this.changeHandler} required/>
            <textarea name="result" className="result" value={result}/>
          </div><br></br>
            
            <button type="submit" className="submit">Generate</button> 
          
        </form>

      </div>
    )
  }
}

export default TextGen
