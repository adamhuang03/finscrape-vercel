"use client";
import React, { useEffect, useState } from "react";
import axios, { AxiosResponse } from 'axios';
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"


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
        const url = process.env.API_URL
        console.log(url)
        setStart(true)
        setEnd(false)
        try {
            
            const res: AxiosResponse<Data> = await axios.post(
                `${url}/api/analysis/betakit/funding`,
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
        <div className="flex-1 flex flex-col w-full max-screen items-center gap-10 mb-10">
            <div className="w-full py-6 font-bold text-slate-50 bg-gradient-to-r from-rose-500 from-50% to-rose-900 px-5 text-center">
                Betakit Fund Article Summarizer
            </div>
            <div className="flex flex-col fade-in word-2 max-w-3xl w-full gap-10 mt-10">
                <div className="flex justify-end gap-2 pt-4">
                    <Input onChange={(e) => setTargetString(e.target.value)} placeholder='Enter your criteria'/>
                    <Button variant="default" onClick={(e) => fetch(targetString)}>Submit</Button>
                </div>
                <div className="flex fade-in word-3 overflow-hidden break-all w-full outline outline-2 outline-offset-4 outline-black/25 rounded-md pl-2 pr-2">
                    {!start && !end && <div>Status: [NOT STARTED] Click submit once you have typed in your criteria.</div>}
                    {start && !end && <div>Status: [IN PROGRESS] Please remain patient, the data is coming!</div>}
                    {data && !start && end && <div>Status: [DONE] Thank you for waiting!</div>}
                </div>
                {!start && end &&
                <div className="flex fade-in flex-col overflow-hidden gap-4 w-full outline outline-2 outline-offset-4 outline-black/25 rounded-md pl-2 pr-2">
                    {data && data.map((item, idx) => {
                        return (
                            <div key={idx} className="divide-y divide-solid">
                                <p><strong>Date:</strong> {item.date}</p>
                                <p><strong>Summary:</strong> {item.summary}</p>
                                <p><strong>Url:</strong> <a href={item.article_url} className="text-blue-700 hover:underline underline-offset-2" target="_blank">{item.article_url}</a></p>
                            </div>
                        )
                    })}
                </div>}
            </div>
            {/* {data && <div>Data fetched: {JSON.stringify(data)}</div>} */}
        </div>
        
    )
}