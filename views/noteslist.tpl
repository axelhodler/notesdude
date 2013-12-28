<div class="container">
  <div class="row">
    <div class="col-md-8">
      <h1>Notes</h1>
      <table class="table">
        <tr>
          <th class="col-md-3">Title</th>
          <th class="col-md-5">Content</th>
          <th></th>
        </tr>
        %for row in rows:
        <tr>
          <td>{{row.get('title')}}</td>
          <td>{{row.get('content')}}</td>
          <td><form action="/delete/{{row.get('id')}}">
          %if user is not None:
              <input class="btn btn-danger btn-xs pull-right" type="submit" value="Delete Note">
          %else:
              <input class="btn btn-danger btn-xs pull-right" type="submit" value="Delete Note" disabled="disabled">
          %end
            </form>
          </td>
        </tr>
        %end
      </table>
    </div>
  <div class="col-md-4">
