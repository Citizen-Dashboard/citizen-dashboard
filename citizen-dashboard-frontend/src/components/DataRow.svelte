<script>
    export let item;
    let expanded = false;

    function toggleExpand() {
        expanded = !expanded;
    }
</script>

<div class="data-row">
    <h3>{item.title}</h3>
    <p>{expanded ? item.summary : item.summary.substring(0, 100) + '...'}</p>
    <button on:click={toggleExpand}>
        {expanded ? 'Show Less' : 'Show More'}
    </button>
</div>

<style>
    .data-row {
        border: 1px solid #ccc;
        padding: 1em;
        border-radius: 4px;
        background-color: #f9f9f9;
    }
    h3 {
        margin: 0 0 0.5em 0;
    }
    p {
        margin: 0;
    }
    button {
        margin-top: 0.5em;
        background-color: #007bff;
        color: white;
        border: none;
        padding: 0.5em;
        border-radius: 4px;
        cursor: pointer;
    }
</style>