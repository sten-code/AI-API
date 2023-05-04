import React, { Component, useRef } from 'react'
import '../css/VoiceGen.css'


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
    const textGenerationModels = data['voice-generation'];
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
  const res = await fetch("http://127.0.0.1:5000/voice-generation/generate", {
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
      model: "microsoft/speecht5-tts",
      models:"",
      result: "",
      seed: 42,
      prompt: "What phrase to do want to have spoken out?",
      samplerate: 16000
    }
  }
  changeAudio = (source) => {
    this.setState({ result: source },function(){
         this.refs.audio.pause();
         this.refs.audio.load();
         this.refs.audio.play();
    })
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
    const { prompt, model, seed, samplerate} = this.state;
    const config = {seed, samplerate};
    const data = { prompt, model, config };
    const jsonData = JSON.stringify(data);
    console.log(jsonData);
    getResult(jsonData).then((resultg) => {
       this.changeAudio(resultg)
        console.log(resultg)
    })

  }
  render() {
    const { prompt, model, seed, samplerate, result, models} = this.state;
    return (
      
      <div>
        
        <form onSubmit={this.submitHandler} className="form" >
          
          <div className='config'>
            
            <div className='input_field'>
                Model: 
                <select name="model" className='input-box' value={model} onChange={this.changeHandler}  dangerouslySetInnerHTML={{ __html: models }}></select>
            </div> 
            
            <div className='input_field'>
                Samplerate: 
                <input type="number" name="samplerate" value={samplerate} onChange={this.changeHandler} className='input-box'/>
            </div> 
          
            <div className='input_field'>
                Seed: 
                <input name="seed" type="number" className='input-box' value={seed} onChange={this.changeHandler} />
            </div> 
          
          </div><br></br>
          
          <div className='ask'>
            <textarea type="text" className="question" name="prompt" value={prompt} onChange={this.changeHandler} required/>
            <div className="result">
                <audio controls ref="audio">
                <source src={result}  type="audio/mpeg"/>
                    Your browser does not support the audio element.
                </audio>
            </div> 
          </div><br></br>
            
            <button type="submit" className="submit">Generate</button> 
          
        </form>

      </div>
    )
  }
}

export default ImageGen