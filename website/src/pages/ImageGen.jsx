import React, { Component } from 'react'
import '../css/ImageGen.css'

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

const modelOptions = async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/models');
    const data = await res.json();
    const textGenerationModels = data['image-generation'];
    const options = textGenerationModels.map((a) => { 
      return ('<option name="' + a +'">' + a + "</option> "   ) 
    });
    return options.join(" ");
  } catch (error) {
    console.error(error);
    return "";
  }
}

const getResult = async (jsonData) => { 
  const res = await fetch("http://127.0.0.1:5000/image-generation/generate", {
      method: 'POST',
      body: jsonData,
      headers: {
        'Content-Type': 'application/json'
      }
    })
  const data = await res.json();
  console.log(data)
  const generatedText = data.format.concat(data.base64)
  if (generatedText.constructor.name === "Array") {
      const result = generatedText.map((a) => {
          return a.generated_text
      })
      return result.join("\n")
  } else {
      return generatedText
  }
}




export class ImageGen extends Component {
  constructor(props) {
    super(props)
  
    this.state = {
      num_inference_steps: 75,
      guidance_scale: 7.5,
      model: "runwayml/stable-diffusion-v1-5",
      models:"",
      result: "",
      seed: 42,
      prompt: "What image do you want to generate?"
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
    const { prompt, model, seed, guidance_scale, num_inference_steps} = this.state;
    const config = {num_inference_steps, seed, guidance_scale};
    const data = { prompt, model, config };
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
    getResult(jsonData).then((resultg) => {
        this.setState({result: resultg})
    })

  }
  render() {
    const { prompt, model, seed, guidance_scale, num_inference_steps, models, result} = this.state;
    return (
      
      <div>
        
        <form onSubmit={this.submitHandler} className="form" >
          
          <div className='config'>
            
            <div className='input_field'>
                Model: 
                <select name="model" className='input-box' value={model} onChange={this.changeHandler}  dangerouslySetInnerHTML={{ __html: models }}></select>
            </div> 
            
            <div className='input_field'>
                Steps: 
                <input type="number" name="num_inference_steps" min="25" max="999" value={num_inference_steps} onChange={this.changeHandler} className='input-box'/>
            </div> 
          
            <div className='input_field'>
                Seed: 
                <input name="seed" type="number" className='input-box' value={seed} onChange={this.changeHandler} />
            </div> 
            <div className='input_field'>
                Guidence scale: 
                <input type="number" name="guidance_scale" className='input-box' value={guidance_scale} onChange={this.changeHandler} />
            </div> 
          
          </div><br></br>
          
          <div className='ask'>
            <textarea type="text" className="question" name="prompt" value={prompt} onChange={this.changeHandler} required/>
            <div className="result"><img src={result} alt="Your generated image her"/></div> 
          </div><br></br>
            
            <button type="submit" className="submit">Generate</button> 
          
        </form>

      </div>
    )
  }
}

export default ImageGen