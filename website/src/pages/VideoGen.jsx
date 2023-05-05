import React, { Component } from 'react'
import '../css/VideoGen.css'
import video from "../video's/Sample.mp4"


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
    const textGenerationModels = data['video-generation'];
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
  const res = await fetch("http://127.0.0.1:5000/video-generation/generate", {
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
      model: "damo-vilab/text-to-video-ms-1.7b",
      models:"",
      result: video,
      seed: 42,
      prompt: "What video do you want?",
      num_frames: 20,
      num_inference_steps: 50,
      fps: 8
    }
  }
  changeVideo = (source) => {
    this.setState({ result: source})
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
    const { prompt, model, seed, num_frames, num_inference_steps, fps} = this.state;
    const config = {seed, num_frames, num_inference_steps, fps};
    const data = { prompt, model, config };
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
    getResult(jsonData).then((resultg) => {
      this.setState({ result: resultg})
    })

  }
  render() {
    const { prompt, model, seed, num_frames, num_inference_steps, result, models, videoKey, fps} = this.state;
    return (
      
      <div>
        
        <form onSubmit={this.submitHandler} className="form" >
          
          <div className='config'>
            
            <div className='input_field'>
                Model: 
                <select name="model" className='input-box' value={model} onChange={this.changeHandler}  dangerouslySetInnerHTML={{ __html: models }}></select>
            </div> 
            
          
            <div className='input_field'>
                Seed: 
                <input name="seed" type="number" className='input-box' value={seed} onChange={this.changeHandler} />
            </div> 
            <div className='input_field'>
                Frames: 
                <input name="num_frames" type="number" className='input-box' value={num_frames} onChange={this.changeHandler} />
            </div> 
            <div className='input_field'>
                Steps: 
                <input name="num_inference_steps" type="number" className='input-box' value={num_inference_steps} onChange={this.changeHandler} />
            </div> 
            <div className='input_field'>
                Fps: 
                <input name="fps" type="number" className='input-box' value={fps} onChange={this.changeHandler} />
            </div> 
          
          </div><br></br>
          
          <div className='ask'>
            <textarea type="text" className="question" name="prompt" value={prompt} onChange={this.changeHandler} required/>
            <div className="result">
              
            <video src={result} type="video/mp4" controls/>
   
            </div> 
          </div><br></br>
            
            <button type="submit" className="submit">Generate</button> 
          
        </form>

      </div>
    )
  }
}

export default ImageGen