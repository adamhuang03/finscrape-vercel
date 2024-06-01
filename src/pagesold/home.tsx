import React, { useEffect, useState } from "react";
import axios, { AxiosResponse } from 'axios';

interface DataItem {
    date: string;
    title_description: string;
    article_url: string;
    article_elements: string[];
    summary: string;
}

type Data = DataItem[];

export default function Page() {
    const [data, setData] = useState<Data | null>(null);
    const [start, setStart] = useState(false);
    const [end, setEnd] = useState(false);
    const [targetString, setTargetString] = useState('');

    // useEffect(() => {
    //     async function fetchUser() {
    //         const res: AxiosResponse = await axios.post(
    //             'http://127.0.0.1:8000/api/analysis/betakit/funding/',
    //             {
    //                 'target_string':
    //             }
    //         );

            
    //     }

    //     fetchUser();
    // }, []);

    useEffect(() => {
        if (data !== null) {
            // console.log(`Data has been set: ${JSON.stringify(data)}`);
            console.log(data)
        }
    }, [data]);

    const fetch = async (targetString: string) => {
        console.log('here')
        setStart(true)
        setEnd(false)
        try {
            const res: AxiosResponse<Data> = await axios.post(
                'http://127.0.0.1:8000/api/analysis/betakit/funding',
                {
                    'target_string': targetString
                }
            );
            const dataArray = Object.values(res.data)
            setData(dataArray)
            setStart(false)
            setEnd(true)
            console.log(`OG Data: ${typeof res.data}`) 
            console.log(res.data) 
        } catch (error) {
            console.error('Error fetching data:', error);
        }

    }// companies raising more than 50 million  

    return (
        <div className="flex-1 flex flex-col w-full max-screen items-center gap-20">
            <div className="w-full py-6 font-bold text-black bg-violet-200 px-5 text-center">
                Betakit Fund Article Summarizer
            </div>
            <input type="text" onChange={(e) => setTargetString(e.target.value)} placeholder='Enter your criteria'/>
            <button type="button" onClick={(e) => fetch(targetString)}>Submit</button>
            <div>Status:</div>
            {!start && !end && <div>[NOT STARTED] Click submit once you have typed in your criteria.</div>}
            {start && !end && <div>[IN PROGRESS] Please remain patient, the data is coming!</div>}
            {data && !start && end && <div>[DONE] Thank you for waiting!</div>}
            {data && !start && end &&
            data.map((item, idx) => {
                return (
                    <div key={idx} className="divide-y divide-solid">
                        <p><strong>Date:</strong> {item.date}</p>
                        <p><strong>Summary:</strong> {item.summary}</p>
                        <p><strong>Url:</strong> {item.article_url}</p>
                    </div>
                )
            })}
            {/* {data && <div>Data fetched: {JSON.stringify(data)}</div>} */}
        </div>
        
    )
}