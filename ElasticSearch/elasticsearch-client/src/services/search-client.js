export async function getSearchResults(queryTerm) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_elasticSearchServer}/search?query=${encodeURIComponent(queryTerm)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        console.log(new Error(`HTTP error! status: ${response.status}`));
        return {
            results: []
        }
    }
    else {
        return await response.json();
    }
}