import React from "react";
import eye from './components/ankh.png';

function About(){
    return(
        <div style={{color:"white", fontFamily:"'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", fontSize:"30px", margin:"30px"}}>
            <div style={{textAlign:"center"}}><img src={eye} alt="ANKH logo" style={{height:"180px", width:"300px"}}></img><h1>MoodTune</h1></div>
            <p>This Project focuses on music for all emotions , whether you are happy sad or suffering a heart break <br></br>
                our app doesnt need to be told anything it reads you emotion like a friend and plays a song to sothen your heart.
            </p>
            Team members:
            <ul>
                <li>
                    240173116003 Devasya Patel
                </li>
                <li>
                    240173116005 Om Kapoor
                </li>
                <li>
                    240173116012 Kamya Shah
                </li>
                <li>
                    240173116013 Mahee Shah
                </li>
            </ul>

        </div>
    );
}

export default About;
