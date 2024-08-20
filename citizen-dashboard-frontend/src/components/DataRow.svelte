<script>
    export let item;
    let expanded = false;

    function toggleExpand() {
        expanded = !expanded;
    }

    function renderAttributeValue(attribute, value) {
        if (value === null) {
            return 'Null';
        } else if (typeof value === 'object') {
            return Object.keys(value).map(key => {
                if (key === 'default') {
                    return value[key];
                } else {
                    return `${key}: ${value[key]}`;
                }
            }).join(', ');
        } else {
            return value;
        }
    }
</script>

<div class="data-row">
    <h3>{item.item_id}</h3>
    {#each Object.keys(item) as attribute}
        {#if attribute !== 'item_id'}
            <div>
                <h4>{attribute}</h4>
                <p>{renderAttributeValue(attribute, item[attribute])}</p>
            </div>
        {/if}
    {/each}
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
    h4 {
        margin: 0 0 0.2em 0;
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