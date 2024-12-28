import styled from "styled-components";
import { React, useState, useMemo } from "react";
import { useQuery } from "react-query";
import { useNavigate, useNavigation, useMatch } from 'react-router-dom';
import { ColumnDef, getCoreRowModel, useReactTable, flexRender, Row } from '@tanstack/react-table';
import { getBitcoin, getBitcoinAx, getInterest } from "../api";



const Wrapper  = styled.div`
    background: black;
`

const Loader = styled.div`
    height: 20vh;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
`;


const Banner = styled.div`
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px;
    background-image: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 1)) , url(${props => props.bgPhoto}); 
    background-size: cover;
`;

const Title = styled.h2`
    font-size: 68px;
    margin-bottom: 20px;
`;

function Home() {
    const navigate = useNavigate();
    const {data, isLoading, isError, error} = useQuery(['interest'], getInterest);

    if (!isLoading) {
        console.log(data.result);

    }

    return <Wrapper>
        {isLoading ? 
        <Loader>Loading</Loader> :
        <>
            <Title>title</Title>
        </>
        }
    </Wrapper>;
}

export default Home;