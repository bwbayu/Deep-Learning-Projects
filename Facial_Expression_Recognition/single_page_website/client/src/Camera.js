import React, { useRef, useState, useCallback, useEffect } from "react";
import Webcam from "react-webcam";
import axios from 'axios';

// define window video
const videoConstraints = {
    width: 480,
    height: 360,
    facingMode: 'environment'
};

const Camera = () => {
    const webcamRef = useRef(null); // ?
    const [isPredicting, setIsPredicting] = useState(false); // state untuk mengatur prediksinya lanjut atau berhenti
    const [resultData, setResultData] = useState(null); // state untuk menyimpan result data hasil prediksi

    // ganti state prediksi ke on / lanjutin prediksi
    const startPrediction = useCallback(() => {
        setIsPredicting(true);
    }, []);

    // ganti state prediksi ke off / prediksi berhenti
    const stopPrediction = useCallback(() => {
        setIsPredicting(false);
        fetchResultData(); // ambil result data hasil prediksi
    }, []);

    // ngirim data image dari react ke flask
    const sendImageToBackend = async (imageSrc) => {
        try {
            const response = await axios.post('process_frame', { //manggil endpoint untuk prediksi model
                image: imageSrc, // imagenya
            });
            console.log('Backend response:', response.data);
        } catch (error) {
            console.error('Error sending image to backend:', error);
        }
    };

    // ambil result data hasil prediksi
    const fetchResultData = async () => {
        try {
            const response = await axios.get('result'); //manggil endpoint untuk ambil data result
            console.log('Result data:', response.data);
            setResultData(response.data); // ganti state resultdata diisi pake data return api
        } catch (error) {
            console.error('Error fetching result data:', error);
        }
    };

    // dipake buat looping kalau state prediksinya true, kirim image ke flask buat input model
    useEffect(() => {
        let intervalId;

        if (isPredicting) {
            intervalId = setInterval(() => {
                const imageSrc = webcamRef.current.getScreenshot();
                console.log("PREDICT" + imageSrc);
                sendImageToBackend(imageSrc);
            }, 5000); // 5 detik
        }

        return () => {
            clearInterval(intervalId);
        };
    }, [isPredicting]);

    return (
        <>
            <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
            />
            <button onClick={startPrediction}>Start Prediction</button>
            <button onClick={stopPrediction}>Stop Prediction</button>
            {resultData && (
                <div>
                    <p>Count Result Data:</p>
                    <ul>
                        {Object.entries(resultData.emotion_counts).map(([label, count]) => (
                            <li key={label}>
                                {label}: {count}
                            </li>
                        ))}
                    </ul>
                    <p>Percentage Result Data:</p>
                    <ul>
                        {Object.entries(resultData.percentage_distribution).map(([label, percentage]) => (
                            <li key={label}>
                                {label}: {percentage.toFixed(2)}%
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </>
    );
};

export default Camera;
