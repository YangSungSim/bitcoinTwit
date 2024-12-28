import axios from "axios";

export function getBitcoin() {
    return fetch(`/dashboard/bitcoin`).then(
        response => response.json()
    )
}

export function getEtf() {
    return fetch(`/dashboard/etf`).then(
        response => response.json()
    )
}

export function getInterest() {
    return fetch(`/dashboard/interest`).then(
        response => response.json()
    )
}

export function getKoreaBond() {
    return fetch(`/dashboard/korea-bond`).then(
        response => response.json()
    )
}

export function getP2p() {
    return fetch(`/dashboard/p2p`).then(
        response => response.json()
    )
}

export function getRealEstate() {
    return fetch(`/dashboard/realestate`).then(
        response => response.json()
    )
}

export function getUsBond() {
    return fetch(`/dashboard/us_bond`).then(
        response => response.json()
    )
}

export function getUsIndex() {
    return fetch(`/dashboard/us_index`).then(
        response => response.json()
    )
}

export function getBitcoinAx() {
    axios.get(`/dashboard/bitcoin`)
    .then((res) => {
        console.log(res);
        return res
    })
    .catch((err) => {
        console.log('에러:   ', err);
    })
}