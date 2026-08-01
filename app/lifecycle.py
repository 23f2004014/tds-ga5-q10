import json

from fastapi import HTTPException



def execute_results(
    task,
    results
):


    stored=json.loads(
        task.artifacts
    )


    proposals = {

        p["packageId"]:
        p

        for p in stored["proposals"]

    }



    executions=[]



    for result in results["results"]:


        package_id = result["packageId"]



        if package_id not in proposals:

            raise HTTPException(
                400,
                "Invalid package"
            )


        proposal = proposals[
            package_id
        ]



        if (
            proposal["actionId"]
            !=
            result["actionId"]
        ):

            raise HTTPException(
                400,
                "Action mismatch"
            )



        if (
            proposal["action"]
            !=
            result["action"]
        ):

            raise HTTPException(
                400,
                "Action mismatch"
            )



        if result["outcome"]=="ACCEPTED":


            executions.append({

                "packageId":
                package_id,


                "actionId":
                result["actionId"],


                "action":
                result["action"],


                "receiptNonce":
                result["receiptNonce"],


                "facts":
                proposal["facts"],


                "evidenceRefs":
                proposal["evidenceRefs"]

            })



    return {

        "batchId":
        results["batchId"],


        "executions":
        executions

    }